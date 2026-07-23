from fastapi import HTTPException, status
from mawaqit.repositories.subcategory import SubCategoryRepository
from mawaqit.models.subcategory import SubCategory
from mawaqit.repositories.category import CategoryRepository

class SubCategoryService:
    def __init__(self, repo: SubCategoryRepository, category_repo: CategoryRepository):
        self.repo = repo
        self.category_repo = category_repo

    async def get_all(self, page: int, page_size: int, category_id: int | None = None) -> tuple[list[SubCategory], int]:
        return await self.repo.get_all(page, page_size, category_id)

    async def get_by_id(self, subcategory_id: int) -> SubCategory:
        subcategory = await self.repo.get_by_id(subcategory_id)
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")
        return subcategory

    async def create(self, title: str, category_id: int, description: str | None) -> SubCategory:
        # Check category exists
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
        # Check unique title
        existing = await self.repo.get_by_title(title)
        if existing:
            raise HTTPException(status_code=400, detail="Subcategory title already exists")
        return await self.repo.create(title, category_id, description)

    async def update(self, subcategory_id: int, title: str | None, category_id: int | None, description: str | None) -> SubCategory:
        subcategory = await self.get_by_id(subcategory_id)
        if title is not None:
            existing = await self.repo.get_by_title(title)
            if existing and existing.id != subcategory_id:
                raise HTTPException(status_code=400, detail="Subcategory title already exists")
        if category_id is not None:
            category = await self.category_repo.get_by_id(category_id)
            if not category:
                raise HTTPException(status_code=400, detail="Category not found")
        return await self.repo.update(subcategory, title, category_id, description)

    async def delete(self, subcategory_id: int):
        subcategory = await self.get_by_id(subcategory_id)
        has_videos = await self.repo.has_article_videos(subcategory_id)
        if has_videos:
            raise HTTPException(
                status_code=400,
                detail="Delete all article/videos in this subcategory first"
            )
        await self.repo.delete(subcategory)