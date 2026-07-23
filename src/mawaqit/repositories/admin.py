from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from mawaqit.models.admin import Admin

class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Admin | None:
        result = await self.session.execute(select(Admin).where(Admin.username == username))
        return result.scalar_one_or_none()

    async def get_by_id(self, username: str) -> Admin | None:
        return await self.get_by_username(username)