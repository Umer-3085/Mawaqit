from fastapi import HTTPException, status
from mawaqit.repositories.category import CategoryRepository
from mawaqit.models.category import Category

class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def get_all(self, page: int, page_size: int) -> tuple[list[Category], int]:
        return await self.repo.get_all(page, page_size)

    async def get_by_id(self, category_id: int) -> Category:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    async def create(self, title: str, description: str | None) -> Category:
        existing = await self.repo.get_by_title(title)
        if existing:
            raise HTTPException(status_code=400, detail="Category title already exists")
        return await self.repo.create(title, description)

    async def update(self, category_id: int, title: str | None, description: str | None) -> Category:
        category = await self.get_by_id(category_id)
        if title is not None:
            existing = await self.repo.get_by_title(title)
            if existing and existing.id != category_id:
                raise HTTPException(status_code=400, detail="Category title already exists")
        return await self.repo.update(category, title, description)

    async def delete(self, category_id: int):
        category = await self.get_by_id(category_id)
        has_videos = await self.repo.has_article_videos(category_id)
        if has_videos:
            raise HTTPException(
                status_code=400,
                detail="Delete all article/videos in this category first"
            )
        await self.repo.delete(category)