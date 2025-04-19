from fastapi import APIRouter, Depends

from wallet.setup.auth import (
    AuthenticatedAccount,
    AuthorizedAccount,
    create_token,
)
from wallet.setup.dependencies import SessionDep, UserServiceDep
from wallet.setup.permissions import Authenticated
from wallet.users.schemas import GetTokenSchema, RegisterUserSchema, UserSchema

users_routers = APIRouter(prefix="/users", tags=["Пользватели"])


@users_routers.post("/get_token")
async def get_token(
    schema: GetTokenSchema, service: UserServiceDep, session: SessionDep
):
    user = await service.authorize(schema, session)
    token = await create_token(user.id)

    return token


@users_routers.post("")
async def register_user(
    schema: RegisterUserSchema, service: UserServiceDep, session: SessionDep
) -> UserSchema:
    user = await service.create_user(schema, session)

    return UserSchema.model_validate(user)


@users_routers.get(
    "",
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
def get_my_data(me: AuthenticatedAccount):
    return UserSchema.model_validate(me)


@users_routers.get("/{id}")
async def get_user_by_id(
    id: int, service: UserServiceDep, session: SessionDep
) -> UserSchema:
    return await service.find_by_id(id, session)
