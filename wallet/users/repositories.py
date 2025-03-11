from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from wallet.users.models import UserModel

class UserRepository:
    async def find_by_name(self, name: str, session: AsyncSession):
        s = await session.execute(Select(UserModel).where(UserModel.name == name))
        return s.scalar_one_or_none()


    async def find_by_id(self, id: int, session: AsyncSession):
        return await session.get(UserModel, id)