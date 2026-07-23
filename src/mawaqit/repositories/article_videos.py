from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from mawaqit.models.article_videos import ArticleVideo
from mawaqit.models.category import Category
from mawaqit.models.subcategory import SubCategory
from typing import Literal

class ArticleVideoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> ArticleVideo | None:
        return await self.db.get(ArticleVideo, id)

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        category_id: int | None = None,
        subcategory_id: int | None = None,
        content_type: Literal["all", "video", "article"] = "all"
    ) -> tuple[list[ArticleVideo], int]:
        page_size = min(page_size, 100)
        offset = (page - 1) * page_size
        
        query = select(ArticleVideo).order_by(ArticleVideo.id.desc())
        
        if category_id:
            query = query.where(ArticleVideo.category_id == category_id)
        if subcategory_id:
            query = query.where(ArticleVideo.subcategory_id == subcategory_id)
        if content_type == "video":
            query = query.where(ArticleVideo.link.isnot(None))
        elif content_type == "article":
            query = query.where(ArticleVideo.link.is_(None))
        
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = list(result.scalars().all())
        
        count_query = select(func.count(ArticleVideo.id))
        if category_id:
            count_query = count_query.where(ArticleVideo.category_id == category_id)
        if subcategory_id:
            count_query = count_query.where(ArticleVideo.subcategory_id == subcategory_id)
        if content_type == "video":
            count_query = count_query.where(ArticleVideo.link.isnot(None))
        elif content_type == "article":
            count_query = count_query.where(ArticleVideo.link.is_(None))
        
        total = await self.db.scalar(count_query)
        return items, total

    async def create(self, title: str, category_id: int, detail: str | None = None, 
                     subcategory_id: int | None = None, link: str | None = None) -> ArticleVideo:
        av = ArticleVideo(title=title, category_id=category_id, detail=detail, 
                          subcategory_id=subcategory_id, link=link)
        self.db.add(av)
        await self.db.commit()
        await self.db.refresh(av)
        return av

    async def update(self, av: ArticleVideo, title: str | None = None, detail: str | None = None,
                     category_id: int | None = None, subcategory_id: int | None = None,
                     link: str | None = None) -> ArticleVideo:
        if title is not None: av.title = title
        if detail is not None: av.detail = detail
        if category_id is not None: av.category_id = category_id
        if subcategory_id is not None: av.subcategory_id = subcategory_id
        if link is not None: av.link = link
        await self.db.commit()
        await self.db.refresh(av)
        return av

    async def delete(self, av: ArticleVideo):
        await self.db.delete(av)
        await self.db.commit()