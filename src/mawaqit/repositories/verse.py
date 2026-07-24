from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from mawaqit.models.verse import Verse
from typing import Optional

class VerseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_composite_key(self, surah_number: int, number_in_surah: int) -> Verse | None:
        return await self.db.get(Verse, {"surah_number": surah_number, "number_in_surah": number_in_surah})

    async def get_by_global_number(self, global_number: int) -> Verse | None:
        result = await self.db.execute(select(Verse).where(Verse.global_number == global_number))
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, page_size: int = 20, **filters) -> tuple[list[Verse], int]:
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        
        query = select(Verse).order_by(Verse.surah_number, Verse.number_in_surah)
        
        # Apply filters
        if filters.get("surah_number"):
            query = query.where(Verse.surah_number == filters["surah_number"])
        if filters.get("juz"):
            query = query.where(Verse.juz == filters["juz"])
        if filters.get("manzil"):
            query = query.where(Verse.manzil == filters["manzil"])
        if filters.get("page_no"):
            query = query.where(Verse.page_no == filters["page_no"])
        if filters.get("ruku"):
            query = query.where(Verse.ruku == filters["ruku"])
        if filters.get("hizb_quarter"):
            query = query.where(Verse.hizb_quarter == filters["hizb_quarter"])
        if filters.get("sajda") is not None:
            query = query.where(Verse.sajda == filters["sajda"])
        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            query = query.where(Verse.arabic.ilike(search_term))
        
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())
        
        # Count query
        count_query = select(func.count(Verse.global_number))
        # Apply same filters to count
        if filters.get("surah_number"):
            count_query = count_query.where(Verse.surah_number == filters["surah_number"])
        if filters.get("juz"):
            count_query = count_query.where(Verse.juz == filters["juz"])
        if filters.get("manzil"):
            count_query = count_query.where(Verse.manzil == filters["manzil"])
        if filters.get("page_no"):
            count_query = count_query.where(Verse.page_no == filters["page_no"])
        if filters.get("ruku"):
            count_query = count_query.where(Verse.ruku == filters["ruku"])
        if filters.get("hizb_quarter"):
            count_query = count_query.where(Verse.hizb_quarter == filters["hizb_quarter"])
        if filters.get("sajda") is not None:
            count_query = count_query.where(Verse.sajda == filters["sajda"])
        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            count_query = count_query.where(Verse.arabic.ilike(search_term))
        
        total = await self.db.scalar(count_query)
        return items, total

    async def get_by_surah(self, surah_number: int) -> list[Verse]:
        """Get all verses for a surah (no pagination)"""
        result = await self.db.execute(
            select(Verse)
            .where(Verse.surah_number == surah_number)
            .order_by(Verse.number_in_surah)
        )
        return list(result.scalars().all())
