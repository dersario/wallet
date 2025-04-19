import os

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from wallet.setup.exceptions import EntityAlreadyExistsException, NotFoundException
from wallet.users.models import UserModel
from wallet.users.repositories import UserRepository
from wallet.users.schemas import GetTokenSchema, RegisterUserSchema

load_dotenv()

TOKEN_SECRET = os.getenv("TOKEN_SECRET")


class UserService:
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    async def create_user(self, schema: RegisterUserSchema, session: AsyncSession):
        user = await self.__repository.find_by_name(schema.name, session)
        if user is not None:
            raise EntityAlreadyExistsException(
                f"User with name={schema.name} already exists"
            )

        user = UserModel(balance=100, name=schema.name, password=schema.password)

        session.add(user)
        await session.commit()

        return user

    async def find_by_id(self, id: int, session: AsyncSession):
        user = await self.__repository.find_by_id(id, session)
        if user is None:
            raise NotFoundException("This user not found")
        return user

    async def find_by_name(self, name: str, session: AsyncSession):
        user = await self.__repository.find_by_name(name, session)
        if user is None:
            raise NotFoundException("This user not found")
        return user

    async def update_balance(
        self, send_id: int, receiver: UserModel, sum: float, session: AsyncSession
    ):
        sender = await self.find_by_id(send_id, session)
        if sender.balance + sum >= 0:
            sender.balance -= sum
            receiver.balance += sum
        else:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Недостаточно средств")

    async def authorize(
        self, schema: GetTokenSchema, session: AsyncSession
    ) -> UserModel:
        user = await self.find_by_name(schema.name, session)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        elif user.password != schema.password:
            raise HTTPException(status.HTTP_418_IM_A_TEAPOT, detail="Wrong password")
        return user
