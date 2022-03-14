# DS Minesweeper

---

### Distributed Systems Spring 2022 Project

#### Game

Found under [game](./game).

This contains the game logic for Minesweeper.

#### Game Server

Found under [game-server](./game-server).

Uses the following environment variables for setup:

```
DS_MAX_WIDTH
    Maximum width for the field, default: 256
    
DS_MAX_WIDTH
    Maximum width for the field, default: 256
    
DS_BROKER_TOKEN
    Auth token to match for requests, default: Throw
    
DS_TESTING
    This is used to enable docs, default: False
    Matches for case insensitive True.
```

Following convenience scripts are available:

```
run_server.sh
    This will run the Minesweeper game server locally.
    
    Environment:
    - DS_BROKER_TOKEN=test
    - DS_TESTING=True
   
run_pytest.sh
    Runs all the pytest tests found in the repo.
    The environment is used in one test that depends 
    on generation speed. Change these if needed.
    
    Environment:
    - DS_TESTING=True
    - DS_MAX_WIDTH=400
    - DS_MAX_HEIGHT=400
```

#### Broker

Found under [broker](./broker).

This also has multiple parts in the root of the repo. This is the main service for this project responsible for
allocating game nodes and deleting them on timeout. The default settings are tuned very conservatively.

The broker and the main compose file use Traefik and Docker API.
__This exposes the raw Docker Socket which is unsafe__

Some security considerations should be taken if this is deployed.

See:

- [compose file](./docker-compose.yml)
- [broker container](./broker.Dockerfile)
- [game node container](./game.Dockerfile)

```
Run this:
$ sh run_broker.sh

Runs the main compose file.
Default lifetime is set to 10 minutes.
Auto cleanup on game end is not yet implemented.

Check the code + compose for environment variables.
```

#### Javascript Client

Found under [client](./client).

Install deps `npm ci` and run `npm start`

#### Python CLI Client

Found under [python-client](./python-client).

```
Requires:
 - requests
 - httpheaders
 - python >= 3.8

How to Run (Requires Running Broker):
$ cd python-client
$ pip install -r requirements.txt
$ python client.py
```