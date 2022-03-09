from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request


class AuthScheme(HTTPBearer):

    def __init__(self):
        super(AuthScheme, self).__init__(
            bearerFormat="Token",
            scheme_name="Auth Token",
            description="Generated Access Token"
        )

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        from .auth import check_auth
        if check_auth(request):
            return HTTPAuthorizationCredentials(scheme="bearer", credentials="")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unauthorized")


__all__ = ["AuthScheme"]
