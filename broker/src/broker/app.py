import asyncio
import logging
import os
import time

import docker
from fastapi import FastAPI, APIRouter, HTTPException, Request, Response

if not os.getenv('DS_IN_CONTAINER'):
    print('Not in container')
    exit(1)

MS = 1000000
MAX_CONTAINERS = int(os.getenv('DS_MAX_NODES', '10'))
MAX_WIDTH = int(os.getenv('DS_MAX_WIDTH', '100'))
MAX_HEIGHT = int(os.getenv('DS_MAX_HEIGHT', '100'))
MAX_LIFETIME = int(os.getenv('DS_LIFETIME', '10'))
PREFIX = os.getenv('DS_PREFIX', 'ds-node')
TESTING = os.getenv('DS_TESTING', 'false').lower() == 'true'
PROJECT = os.getenv('DS_PROJECT', 'distributed-systems-nodes')
NETWORK: str

composer = docker.from_env()
app = FastAPI(
    description='Minesweeper Broker Server. Creates game nodes on demand.',
    title='DS Broker',
    openapi_tags=[
        {
            'name': 'API',
            'description': 'Available API operations'
        }
    ],
    redoc_url=None,
    docs_url='/docs' if TESTING else None
)
api = APIRouter(tags=['API'])

if TESTING:
    def get_env(token, name):
        return {
            'DS_BROKER_TOKEN': token,
            'DS_MAX_WIDTH': MAX_WIDTH,
            'DS_MAX_HEIGHT': MAX_HEIGHT,
            'DS_ROOT_PATH': f'/{name}/',
            'DS_TESTING': 'true',
        }
else:
    def get_env(token, name):
        return {
            'DS_BROKER_TOKEN': token,
            'DS_MAX_WIDTH': MAX_WIDTH,
            'DS_MAX_HEIGHT': MAX_HEIGHT,
            'DS_ROOT_PATH': f'/{name}/',
        }


async def run_reaper():
    net = composer.networks.get(NETWORK)
    while True:
        net.reload()
        for c in net.containers:
            if c.name.startswith(PREFIX):
                start_time = int(c.attrs['Config']['Labels']['ds.start-time'])
                delta = time.time() - start_time
                if delta > MAX_LIFETIME:
                    logging.getLogger('uvicorn').info(f'Reaper - Killing container: {c.name} ({delta:.2f}s)')
                    c.stop(timeout=2)
        await asyncio.sleep(60)


def get_labels(name):
    return {
        'ds.start-time': str(int(time.time())),
        'traefik.enable': 'true',
        f'traefik.http.routers.{name}.rule': f'PathPrefix(`/{name}/`)',
        f'traefik.http.services.{name}.loadbalancer.server.port': '8080',

        f'traefik.http.middlewares.{name}-stripper.stripprefix.prefixes': f'/{name}',

        f'traefik.http.middlewares.{name}-head.headers.accesscontrolalloworiginlist': '*',
        f'traefik.http.middlewares.{name}-head.headers.accesscontrolallowmethods': 'GET,POST,DELETE',
        f'traefik.http.middlewares.{name}-head.headers.accesscontrolexposeheaders': '*',
        f'traefik.http.middlewares.{name}-head.headers.accesscontrolallowheaders': '*',

        f'traefik.http.routers.{name}.middlewares': f'{name}-stripper@docker,{name}-head@docker',

        'com.docker.compose.project': PROJECT,
    }


def random_string():
    from secrets import choice
    from string import ascii_lowercase
    return ''.join(map(lambda _: choice(ascii_lowercase), range(0, 10)))


def get_name():
    from docker.errors import NotFound
    while True:
        name = f'{PREFIX}-{random_string()}'
        try:
            composer.containers.get(name)
        except NotFound:
            break
    return name


def get_token():
    from secrets import token_urlsafe
    return token_urlsafe(32)


def count_containers() -> int:
    return sum(map(lambda c: c.name.startswith(PREFIX), composer.networks.get(NETWORK).containers))


@app.on_event('startup')
async def start():
    global NETWORK, PROJECT

    import socket
    self = composer.containers.get(socket.gethostname())
    net = next(iter(self.attrs['NetworkSettings']['Networks'].keys()))
    NETWORK = net

    app.state.checker = asyncio.get_running_loop().create_task(run_reaper(), name='DS Reaper')


@app.on_event('shutdown')
async def stop():
    net = composer.networks.get(NETWORK)
    for c in net.containers:
        if c.name.startswith(PREFIX):
            c.stop()


@api.post('/start')
def start(r: Request):
    from headers import AUTHORIZATION, LOCATION
    if count_containers() >= MAX_CONTAINERS:
        raise HTTPException(status_code=503)
    name = get_name()
    token = get_token()
    composer.containers.run(
        name=name,
        hostname=name,
        image='ds-gameserver:latest',
        detach=True,
        network=NETWORK,
        environment=get_env(token, name),
        tty=False,
        remove=True,
        mem_limit='40M',
        memswap_limit='50M',
        nano_cpus=int(2E8),
        labels=get_labels(name),
    )
    return Response(status_code=201, headers={
        AUTHORIZATION: f'Bearer {token}',
        LOCATION: f'{r.base_url}{name}/start',
    })


app.include_router(api)
