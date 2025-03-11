from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select

from wallet.transactions.models import TransactionModel
from wallet.users.models import UserModel

class TransactionRepository:
    # async def find_by_name(self, name: str, session: AsyncSession):
    #     s = await session.execute(Select(UserModel).where(UserModel.name == name))
    #     return s.scalar_one_or_none()

    async def get_all_by_sender(self, name:str, session: AsyncSession):
        q = select(TransactionModel).where(TransactionModel.sender == name)
        s = await session.execute(q)
        return list(s.scalars().all())
    
    async def get_all_by_receiver(self, name:str, session: AsyncSession):
        q = select(TransactionModel).where(TransactionModel.receiver == name)
        s = await session.execute(q)
        return list(s.scalars().all())
    

    async def find_by_id(self, id: int, session: AsyncSession):
        return await session.get(TransactionModel, id)