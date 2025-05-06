from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from wallet.setup.dependencies import SessionDep, Token, UserServiceDep
from wallet.setup.permissions import BasePermission
from wallet.users.models import UserModel

SecuritySchema = HTTPBearer(auto_error=False)


async def create_access_token(
    data: dict, token: str, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, token, algorithm="HS256")
    return encoded_jwt


async def create_token(id, token: Token):
    token = await create_access_token({"id": id}, token, timedelta(minutes=30))
    return token


async def authenticate_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(SecuritySchema)
    ],
    token_secret: Token,
    account_service: UserServiceDep,
    session: SessionDep,
) -> UserModel | None:
    if credentials is None:
        return None
    token = credentials.credentials
    user_data = jwt.decode(token, token_secret, algorithms=["HS256"])

    return await account_service.find_by_id(user_data["id"], session)


AuthenticatedAccount = Annotated[UserModel | None, Depends(authenticate_user)]


class AuthorizedAccount:
    def __init__(self, permission: BasePermission):
        self._permission = permission

    def __call__(self, account: AuthenticatedAccount):
        if not self._permission.check_permission(account):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
