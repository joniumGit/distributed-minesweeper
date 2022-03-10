import pytest


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
def scheme(r, run_async):
    from server.auth import AuthScheme
    from fastapi import Request
    from typing import cast

    auth_scheme = AuthScheme()
    yield lambda header: run_async(auth_scheme, cast(Request, r(header)))


def test_import_no_token(token_name, token):
    import server.auth.auth as should_throw
    # Break everything
    from os import environ
    import sys
    import importlib
    environ.pop(token_name, None)

    try:
        with pytest.raises(KeyError):
            if 'server.auth.auth' in sys.modules:
                importlib.reload(sys.modules['server.auth.auth'])
            else:
                import server.auth.auth as should_throw
                print(should_throw)
    finally:
        # Fix everything
        environ[token_name] = token
        import server.auth.auth as fix
        print(fix)
        importlib.reload(fix)


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
