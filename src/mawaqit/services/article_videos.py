from fastapi import HTTPException
from mawaqit.repositories.article_videos import ArticleVideoRepository
from mawaqit.repositories.category import CategoryRepository
from mawaqit.repositories.subcategory import SubCategoryRepository
from mawaqit.models.article_videos import ArticleVideo

class ArticleVideoService:
    def __init__(self, repo: ArticleVideoRepository, cat_repo: CategoryRepository, subcat_repo: SubCategoryRepository):
        self.repo = repo
        self.cat_repo = cat_repo
        self.subcat_repo = subcat_repo

    async def get_all(self, page: int, page_size: int, category_id: int | None = None,
                      subcategory_id: int | None = None, content_type: str = "all"):
        return await self.repo.get_all(page, page_size, category_id, subcategory_id, content_type)

    async def get_by_id(self, id: int) -> ArticleVideo:
        av = await self.repo.get_by_id(id)
        if not av:
            raise HTTPException(status_code=404, detail="Article/Video not found")
        return av

    async def create(self, title: str, category_id: int, detail: str | None = None,
                     subcategory_id: int | None = None, link: str | None = None) -> ArticleVideo:
        # Validate category exists
        cat = await self.cat_repo.get_by_id(category_id)
        if not cat:
            raise HTTPException(status_code=400, detail="Category not found")
        # Validate subcategory if provided
        if subcategory_id:
            subcat = await self.subcat_repo.get_by_id(subcategory_id)
            if not subcat:
                raise HTTPException(status_code=400, detail="Subcategory not found")
            if subcat.category_id != category_id:
                raise HTTPException(status_code=400, detail="Subcategory does not belong to this category")
        return await self.repo.create(title, category_id, detail, subcategory_id, link)

    async def update(self, id: int, title: str | None = None, detail: str | None = None,
                     category_id: int | None = None, subcategory_id: int | None = None,
                     link: str | None = None) -> ArticleVideo:
        av = await self.get_by_id(id)
        if category_id:
            cat = await self.cat_repo.get_by_id(category_id)
            if not cat:
                raise HTTPException(status_code=400, detail="Category not found")
        if subcategory_id is not None:
            if subcategory_id:
                subcat = await self.subcat_repo.get_by_id(subcategory_id)
                if not subcat:
                    raise HTTPException(status_code=400, detail="Subcategory not found")
                cat_id = category_id or av.category_id
                if subcat.category_id != cat_id:
                    raise HTTPException(status_code=400, detail="Subcategory does not belong to this category")
            # Allow setting to NULL (remove subcategory)
        return await self.repo.update(av, title, detail, category_id, subcategory_id, link)

    async def delete(self, id: int):
        av = await self.get_by_id(id)
        await self.repo.delete(av)