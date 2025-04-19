import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from wallet.setup.dependencies import SessionDep, UserServiceDep
from wallet.setup.permissions import BasePermission
from wallet.users.models import UserModel

SecuritySchema = HTTPBearer(auto_error=False)


load_dotenv()

TOKEN_SECRET = os.getenv("TOKEN_SECRET")


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET, algorithm="HS256")
    return encoded_jwt


async def create_token(
    id,
):
    token = await create_access_token({"id": id}, timedelta(minutes=30))
    return token


async def authenticate_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(SecuritySchema)
    ],
    account_service: UserServiceDep,
    session: SessionDep,
) -> UserModel | None:
    if credentials is None:
        return None
    token = credentials.credentials
    user_data = jwt.decode(token, TOKEN_SECRET, algorithms=["HS256"])

    return await account_service.find_by_id(user_data["id"], session)


AuthenticatedAccount = Annotated[UserModel | None, Depends(authenticate_user)]


class AuthorizedAccount:
    def __init__(self, permission: BasePermission):
        self._permission = permission

    def __call__(self, account: AuthenticatedAccount):
        if not self._permission.check_permission(account):
            raise HTTPException(status.HTTP_403_FORBIDDEN)
