from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from wallet.users.models import UserModel


class UserRepository:
    async def find_by_name(self, name: str, session: AsyncSession):
        q = select(UserModel).where(UserModel.name == name)
        s = await session.execute(q)

        return s.scalar_one_or_none()

    async def find_by_id(self, id: int, session: AsyncSession):
        return await session.get(UserModel, id)
