from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from mawaqit.models.detail import TranslationTafseerDetail

class TranslationTafseerDetailRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> TranslationTafseerDetail | None:
        return await self.db.get(TranslationTafseerDetail, id)

    async def get_all(self, page: int = 1, page_size: int = 20,
                      lang: str | None = None,
                      direction: str | None = None,
                      author: str | None = None,
                      search: str | None = None) -> tuple[list[TranslationTafseerDetail], int]:
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size

        query = select(TranslationTafseerDetail).order_by(TranslationTafseerDetail.id)

        if lang:
            query = query.where(TranslationTafseerDetail.lang == lang)
        if direction:
            query = query.where(TranslationTafseerDetail.direction == direction)
        if author:
            query = query.where(TranslationTafseerDetail.author.ilike(f"%{author}%"))
        if search:
            search_term = f"%{search}%"
            query = query.where(or_(
                TranslationTafseerDetail.title.ilike(search_term),
                TranslationTafseerDetail.author.ilike(search_term),
                TranslationTafseerDetail.description.ilike(search_term)
            ))

        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())

        count_query = select(func.count(TranslationTafseerDetail.id))
        if lang:
            count_query = count_query.where(TranslationTafseerDetail.lang == lang)
        if direction:
            count_query = count_query.where(TranslationTafseerDetail.direction == direction)
        if author:
            count_query = count_query.where(TranslationTafseerDetail.author.ilike(f"%{author}%"))
        if search:
            search_term = f"%{search}%"
            count_query = count_query.where(or_(
                TranslationTafseerDetail.title.ilike(search_term),
                TranslationTafseerDetail.author.ilike(search_term),
                TranslationTafseerDetail.description.ilike(search_term)
            ))
        total = await self.db.scalar(count_query)

        return items, total

    async def get_all_simple(self) -> list[TranslationTafseerDetail]:
        result = await self.db.execute(select(TranslationTafseerDetail).order_by(TranslationTafseerDetail.id))
        return list(result.scalars().all())

    async def get_by_lang(self, lang: str, page: int = 1, page_size: int = 100) -> tuple[list[TranslationTafseerDetail], int]:
        return await self.get_all(page=page, page_size=page_size, lang=lang)

    async def get_by_direction(self, direction: str, page: int = 1, page_size: int = 100) -> tuple[list[TranslationTafseerDetail], int]:
        return await self.get_all(page=page, page_size=page_size, direction=direction)

    async def get_by_author(self, author: str, page: int = 1, page_size: int = 100) -> tuple[list[TranslationTafseerDetail], int]:
        return await self.get_all(page=page, page_size=page_size, author=author)