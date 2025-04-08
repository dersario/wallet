from fastapi import APIRouter, Depends

from wallet.setup.auth import AuthenticatedAccount, AuthorizedAccount
from wallet.setup.dependencies import SessionDep, UserServiceDep
from wallet.setup.permissions import Authenticated
from wallet.users.schemas import RegisterUserSchema, UserSchema

users_routers = APIRouter(prefix="/users", tags=["Пользватели"])


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
async def get_user_by_id(id: int) -> UserSchema:
    return UserSchema(id=1, name="Travor", balance=0)
