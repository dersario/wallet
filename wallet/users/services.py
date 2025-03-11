from sqlalchemy import func, select
from wallet.users.repositories import UserRepository
from fastapi import HTTPException, status
from wallet.users.models import UserModel
from wallet.users.schemas import  RegisterUserSchema
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    async def create_user(self, schema: RegisterUserSchema, session: AsyncSession):
        user = await self.__repository.find_by_name(schema.name, session)
        if user is not None:
            raise HTTPException(status.HTTP_409_CONFLICT)
        
        user = UserModel(balance = 100, name=schema.name, password=schema.password)

        session.add(user)
        await session.commit()

        return user
    
    async def find_by_id(self, id: int, session:AsyncSession):
        user = await session.get(UserModel, id)
        if user is None:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Хто ето")
        return user
    
    async def find_by_name(self, name: str, session:AsyncSession):
        q = select(UserModel).where(UserModel.name == name)
        user = await session.execute(q)
        return user.scalar_one_or_none()

    async def update_balance(self, send_id:int,receiver: UserModel, sum:float, session:AsyncSession):
        sender = await self.find_by_id(send_id,session)
        if sender.balance+sum >= 0:
            sender.balance-=sum
            receiver.balance+=sum
        else:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Недостаточно средств")