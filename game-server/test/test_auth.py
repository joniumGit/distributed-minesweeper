import pytest


def load_auth(token_name, *_):
    from os import environ
    environ.pop(token_name, None)
    try:
        from server.auth import auth as should_throw
        print(should_throw)
    except KeyError:
        exit(0)
    exit(1)


@pytest.fixture
def r():
    from collections import namedtuple
    from headers import AUTHORIZATION
    yield lambda v: namedtuple('Request', 'headers')({AUTHORIZATION: v})


@pytest.fixture
def auth():
    from server.auth import auth
    yield auth


@pytest.fixture
def scheme(r):
    from server.auth import AuthScheme
    from asyncio import new_event_loop
    from fastapi import Request
    from typing import cast

    def run_inside(header: str):
        loop = new_event_loop()
        try:
            auth_scheme = AuthScheme()
            return loop.run_until_complete(auth_scheme(cast(Request, r(header))))
        finally:
            loop.close()

    yield run_inside


def test_import_no_token(token_name):
    import multiprocessing as mp
    p = mp.Process(target=load_auth, args=(token_name,))
    p.start()
    p.join()
    assert p.exitcode == 0


def test_bad_scheme(r, auth):
    assert not auth.check_auth(r('JWT abcd'))


def test_not_partition_ok(r, auth):
    assert not auth.check_auth(r('Bearer'))


def test_bad_value(r, auth, token):
    assert not auth.check_auth(r(f'Bearer {token[:-2]}'))


def test_ok(r, auth, token):
    assert auth.check_auth(r(f'bearer {token}'))


def test_no_header(r, auth):
    req = r('')
    req.headers.clear()
    assert not auth.check_auth(req)


def test_not_ascii(r, auth):
    assert not auth.check_auth(r('Bearer ööööö'))


def test_bad_scheme_throws(scheme):
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        scheme('JWT abcd')


def test_get_credentials(scheme, token):
    cred = scheme(f'Bearer {token}')
    assert cred.scheme == 'bearer'
    assert cred.credentials == ''
