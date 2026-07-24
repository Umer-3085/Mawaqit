from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from mawaqit.models.surah import Surah

class SurahRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_number(self, surah_number: int) -> Surah | None:
        return await self.db.get(Surah, surah_number)

    async def get_all(self, page: int = 1, page_size: int = 20, 
                      revelation_type: str | None = None, 
                      search: str | None = None) -> tuple[list[Surah], int]:
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        
        query = select(Surah).order_by(Surah.surah_number)
        
        if revelation_type and revelation_type != "all":
            query = query.where(Surah.revelation_type == revelation_type)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(or_(
                Surah.name_arabic.ilike(search_term),
                Surah.english_name.ilike(search_term),
                Surah.english_name_translation.ilike(search_term)
            ))
        
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())
        
        count_query = select(func.count(Surah.surah_number))
        if revelation_type and revelation_type != "all":
            count_query = count_query.where(Surah.revelation_type == revelation_type)
        if search:
            search_term = f"%{search}%"
            count_query = count_query.where(or_(
                Surah.name_arabic.ilike(search_term),
                Surah.english_name.ilike(search_term),
                Surah.english_name_translation.ilike(search_term)
            ))
        total = await self.db.scalar(count_query)
        
        return items, total

    async def get_all_simple(self) -> list[Surah]:
        """Lightweight list for dropdowns - no pagination"""
        result = await self.db.execute(select(Surah).order_by(Surah.surah_number))
        return list(result.scalars().all())
