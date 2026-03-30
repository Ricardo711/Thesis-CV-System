from __future__ import annotations

from fastapi import Cookie, Header, HTTPException, status

from app.core.security import decode_token
from app.services.users_service import UsersService


def _extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) != 2:
        return None
    scheme, token = parts[0].strip().lower(), parts[1].strip()
    if scheme != "bearer" or not token:
        return None
    return token


async def get_current_user(
    access_token: str | None = Cookie(default=None, alias="access_token"),
    authorization: str | None = Header(default=None, alias="Authorization"),
):

    bearer = _extract_bearer_token(authorization)
    token = bearer or access_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticathed."
        )

    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token."
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token."
        )

    return await UsersService.get_by_id(user_id)
