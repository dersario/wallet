from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from wallet.setup.db import DatabaseManager
from wallet.users.services import UserService


def token_secret(request: Request):
    return cast(str, request.app.state.token_secret)


def user_service(request: Request):
    return cast(UserService, request.app.state.user_service)


async def session(request: Request):
    db_manager = cast(DatabaseManager, request.app.state.db_manager)
    async with db_manager.get_session() as session:
        yield session


Token = Annotated[str, Depends(token_secret)]
UserServiceDep = Annotated[UserService, Depends(user_service)]
SessionDep = Annotated[AsyncSession, Depends(session)]
