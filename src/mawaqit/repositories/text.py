from sqlalchemy import select, func, or_, join
from sqlalchemy.ext.asyncio import AsyncSession
from mawaqit.models.verse_texts import VerseText
from mawaqit.models.detail import TranslationTafseerDetail
from typing import Optional

class VerseTextRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_composite_key(self, surah_number: int, verse_number: int, detail_id: int) -> VerseText | None:
        return await self.db.get(VerseText, {"surah_number": surah_number, "verse_number": verse_number, "detail_id": detail_id})

    async def get_all(self, page: int = 1, page_size: int = 20, **filters) -> tuple[list[VerseText], int]:
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        
        query = select(VerseText).order_by(VerseText.surah_number, VerseText.verse_number, VerseText.detail_id)
        
        if filters.get("surah_number"):
            query = query.where(VerseText.surah_number == filters["surah_number"])
        if filters.get("verse_number"):
            query = query.where(VerseText.verse_number == filters["verse_number"])
        if filters.get("detail_id"):
            query = query.where(VerseText.detail_id == filters["detail_id"])
        if filters.get("has_tafseer") is not None:
            if filters["has_tafseer"]:
                query = query.where(VerseText.verse_tafseer.isnot(None))
            else:
                query = query.where(VerseText.verse_tafseer.is_(None))
        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            query = query.where(or_(
                VerseText.verse_translation.ilike(search_term),
                VerseText.verse_tafseer.ilike(search_term)
            ))
        
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())
        
        count_query = select(func.count(VerseText.surah_number))
        if filters.get("surah_number"):
            count_query = count_query.where(VerseText.surah_number == filters["surah_number"])
        if filters.get("verse_number"):
            count_query = count_query.where(VerseText.verse_number == filters["verse_number"])
        if filters.get("detail_id"):
            count_query = count_query.where(VerseText.detail_id == filters["detail_id"])
        if filters.get("has_tafseer") is not None:
            if filters["has_tafseer"]:
                count_query = count_query.where(VerseText.verse_tafseer.isnot(None))
            else:
                count_query = count_query.where(VerseText.verse_tafseer.is_(None))
        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            count_query = count_query.where(or_(
                VerseText.verse_translation.ilike(search_term),
                VerseText.verse_tafseer.ilike(search_term)
            ))
        total = await self.db.scalar(count_query)
        
        return items, total

    async def get_by_surah(self, surah_number: int, page: int = 1, page_size: int = 20) -> tuple[list[VerseText], int]:
        return await self.get_all(page=page, page_size=page_size, surah_number=surah_number)

    async def get_by_verse(self, surah_number: int, verse_number: int) -> list[VerseText]:
        result = await self.db.execute(
            select(VerseText)
            .where(VerseText.surah_number == surah_number, VerseText.verse_number == verse_number)
            .order_by(VerseText.detail_id)
        )
        return list(result.scalars().all())

    async def get_by_detail(self, detail_id: int, page: int = 1, page_size: int = 20) -> tuple[list[VerseText], int]:
        return await self.get_all(page=page, page_size=page_size, detail_id=detail_id)

    async def get_by_lang(self, lang: str, page: int = 1, page_size: int = 20) -> tuple[list[VerseText], int]:
        # Join with translation_tafseer_details to filter by lang
        from sqlalchemy import join
        j = join(VerseText, TranslationTafseerDetail, VerseText.detail_id == TranslationTafseerDetail.id)
        query = select(VerseText).select_from(j).where(TranslationTafseerDetail.lang == lang).order_by(VerseText.surah_number, VerseText.verse_number, VerseText.detail_id)
        
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())
        
        count_query = select(func.count(VerseText.surah_number)).select_from(j).where(TranslationTafseerDetail.lang == lang)
        total = await self.db.scalar(count_query)
        
        return items, total

    async def get_all_with_details(self, page: int = 1, page_size: int = 20, **filters) -> tuple[list[VerseText], int]:
        """Get verse texts with joined translation detail for nested response"""
        from sqlalchemy import join
        j = join(VerseText, TranslationTafseerDetail, VerseText.detail_id == TranslationTafseerDetail.id, isouter=True)
        query = select(VerseText).select_from(j).order_by(VerseText.surah_number, VerseText.verse_number, VerseText.detail_id)
        
        # Apply same filters as get_all
        if filters.get("surah_number"):
            query = query.where(VerseText.surah_number == filters["surah_number"])
        if filters.get("verse_number"):
            query = query.where(VerseText.verse_number == filters["verse_number"])
        if filters.get("detail_id"):
            query = query.where(VerseText.detail_id == filters["detail_id"])
        if filters.get("has_tafseer") is not None:
            if filters["has_tafseer"]:
                query = query.where(VerseText.verse_tafseer.isnot(None))
            else:
                query = query.where(VerseText.verse_tafseer.is_(None))
        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            query = query.where(or_(
                VerseText.verse_translation.ilike(search_term),
                VerseText.verse_tafseer.ilike(search_term)
            ))
        if filters.get("lang"):
            query = query.where(TranslationTafseerDetail.lang == filters["lang"])
        
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())
        
        count_query = select(func.count(VerseText.surah_number)).select_from(j)
        if filters.get("surah_number"):
            count_query = count_query.where(VerseText.surah_number == filters["surah_number"])
        if filters.get("verse_number"):
            count_query = count_query.where(VerseText.verse_number == filters["verse_number"])
        if filters.get("detail_id"):
            count_query = count_query.where(VerseText.detail_id == filters["detail_id"])
        if filters.get("has_tafseer") is not None:
            if filters["has_tafseer"]:
                count_query = count_query.where(VerseText.verse_tafseer.isnot(None))
            else:
                count_query = count_query.where(VerseText.verse_tafseer.is_(None))
        if filters.get("search"):
            search_term = f"%{filters['search']}%"
            count_query = count_query.where(or_(
                VerseText.verse_translation.ilike(search_term),
                VerseText.verse_tafseer.ilike(search_term)
            ))
        if filters.get("lang"):
            count_query = count_query.where(TranslationTafseerDetail.lang == filters["lang"])
        total = await self.db.scalar(count_query)
        
        return items, total