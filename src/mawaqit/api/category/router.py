from fastapi import APIRouter, Depends, status
from mawaqit.schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse, CategoryList
)
from mawaqit.services.category import CategoryService
from mawaqit.api.deps import get_category_service, get_current_admin

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=CategoryList)
async def list_categories(
    page: int = 1,
    page_size: int = 20,
    service: CategoryService = Depends(get_category_service)
):
    items, total = await service.get_all(page, page_size)
    total_pages = (total + page_size - 1) // page_size
    return CategoryList(
        items=items, total=total, page=page, page_size=page_size, total_pages=total_pages
    )

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    return await service.get_by_id(category_id)

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    _ = Depends(get_current_admin)
):
    return await service.create(data.title, data.description)

@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
    _ = Depends(get_current_admin)
):
    return await service.update(category_id, data.title, data.description)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
    _ = Depends(get_current_admin)
):
    await service.delete(category_id)