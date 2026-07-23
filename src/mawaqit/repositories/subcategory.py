from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from mawaqit.models.subcategory import SubCategory
from mawaqit.models.article_videos import ArticleVideo

class SubCategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, subcategory_id: int) -> SubCategory | None:
        return await self.db.get(SubCategory, subcategory_id)

    async def get_by_title(self, title: str) -> SubCategory | None:
        result = await self.db.execute(select(SubCategory).where(SubCategory.title == title))
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, page_size: int = 20, category_id: int | None = None) -> tuple[list[SubCategory], int]:
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        query = select(SubCategory).order_by(SubCategory.title)
        if category_id:
            query = query.where(SubCategory.category_id == category_id)
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())
        count_query = select(func.count(SubCategory.id))
        if category_id:
            count_query = count_query.where(SubCategory.category_id == category_id)
        total = await self.db.scalar(count_query)
        return items, total

    async def create(self, title: str, category_id: int, description: str | None) -> SubCategory:
        subcategory = SubCategory(title=title, category_id=category_id, description=description)
        self.db.add(subcategory)
        await self.db.commit()
        await self.db.refresh(subcategory)
        return subcategory

    async def update(self, subcategory: SubCategory, title: str | None = None, category_id: int | None = None, description: str | None = None) -> SubCategory:
        if title is not None:
            subcategory.title = title
        if category_id is not None:
            subcategory.category_id = category_id
        if description is not None:
            subcategory.description = description
        await self.db.commit()
        await self.db.refresh(subcategory)
        return subcategory

    async def delete(self, subcategory: SubCategory):
        await self.db.delete(subcategory)
        await self.db.commit()

    async def has_article_videos(self, subcategory_id: int) -> bool:
        result = await self.db.execute(
            select(ArticleVideo.id).where(ArticleVideo.subcategory_id == subcategory_id).limit(1)
        )
        return result.scalar_one_or_none() is not None