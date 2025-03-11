from typing import Any
from fastapi import APIRouter, Depends, status
from wallet.setup.dependencies import SessionDep, UserServiceDep
from wallet.users.models import UserModel
from wallet.users.schemas import UserSchema, RegisterUserSchema
from wallet.setup.permissions import Anonymous, Authenticated
from wallet.setup.auth import AuthenticatedAccount, AuthorizedAccount


users_routers = APIRouter(prefix="/users", tags=["Пользватели"])

@users_routers.post("")
async def register_user(schema: RegisterUserSchema, service: UserServiceDep, session: SessionDep) -> UserSchema:
    user = await service.create_user(schema, session)

    return UserSchema.model_validate(user)

@users_routers.get("",dependencies=[Depends(AuthorizedAccount(Authenticated()))],)
def get_my_data(me: AuthenticatedAccount):
    return UserSchema.model_validate(me)

@users_routers.get("/{id}")
async def get_user_by_id(id: int) -> UserSchema:
    return UserSchema(
        id=1,
        name="Travor",
        balance=0
    )