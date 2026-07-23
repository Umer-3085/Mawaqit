from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from mawaqit.models.category import Category
from mawaqit.models.article_videos import ArticleVideo  # need model

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: int) -> Category | None:
        return await self.db.get(Category, category_id)

    async def get_by_title(self, title: str) -> Category | None:
        result = await self.db.execute(select(Category).where(Category.title == title))
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, page_size: int = 20) -> tuple[list[Category], int]:
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Category).order_by(Category.title).offset(offset).limit(page_size)
        )
        items = list(result.scalars().all())
        total = await self.db.scalar(select(func.count(Category.id)))
        return items, total

    async def create(self, title: str, description: str | None) -> Category:
        category = Category(title=title, description=description)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(self, category: Category, title: str | None = None, description: str | None = None) -> Category:
        if title is not None:
            category.title = title
        if description is not None:
            category.description = description
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category: Category):
        await self.db.delete(category)
        await self.db.commit()

    async def has_article_videos(self, category_id: int) -> bool:
        result = await self.db.execute(
            select(ArticleVideo.id).where(ArticleVideo.category_id == category_id).limit(1)
        )
        return result.scalar_one_or_none() is not None