import os
from secrets import compare_digest
from typing import Any

from headers import AUTHORIZATION

TOKEN = os.getenv('DS_BROKER_TOKEN')
if TOKEN is None:
    raise KeyError('Failed to load key')
else:
    TOKEN = TOKEN.encode('ascii')


def check_auth(r: Any) -> bool:
    auth_header: str = r.headers.get(AUTHORIZATION, None)
    if auth_header is not None:
        scheme, _, value = auth_header.partition(' ')
        if scheme.lower() == 'bearer' and len(value) > 0:
            try:
                return compare_digest(value.encode('ascii'), TOKEN)
            except UnicodeEncodeError:
                pass
    return False
