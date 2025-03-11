from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from wallet.setup.dependencies import SessionDep, UserServiceDep
from wallet.setup.permissions import BasePermission
from wallet.users.models import UserModel


SecuritySchema = HTTPBasic()

async def authenticate_user(
    credentials: Annotated[HTTPBasicCredentials | None, Depends(SecuritySchema)],
    account_service: UserServiceDep,
    session: SessionDep,
) -> UserModel | None:
    if credentials is None:
        return None
    name = credentials.username
    user = await account_service.find_by_name(name, session)
    
    if credentials.password == user.password:
        return user
    
AuthenticatedAccount = Annotated[UserModel | None, Depends(authenticate_user)]

class AuthorizedAccount:
    def __init__(self, permission: BasePermission):
        self._permission = permission

    def __call__(self, account: AuthenticatedAccount):
        if not self._permission.check_permission(account):
            raise HTTPException(status.HTTP_403_FORBIDDEN)