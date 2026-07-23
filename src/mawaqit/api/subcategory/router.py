from fastapi import APIRouter, Depends, status
from mawaqit.schemas.subcategory import (
    SubCategoryCreate, SubCategoryUpdate, SubCategoryResponse, SubCategoryList
)
from mawaqit.services.subcategory import SubCategoryService
from mawaqit.api.deps import get_subcategory_service, get_current_admin

router = APIRouter(prefix="/subcategories", tags=["SubCategories"])

@router.get("", response_model=SubCategoryList)
async def list_subcategories(
    page: int = 1,
    page_size: int = 20,
    category_id: int | None = None,
    service: SubCategoryService = Depends(get_subcategory_service)
):
    items, total = await service.get_all(page, page_size, category_id)
    total_pages = (total + page_size - 1) // page_size
    return SubCategoryList(
        items=items, total=total, page=page, page_size=page_size, total_pages=total_pages
    )

@router.get("/{subcategory_id}", response_model=SubCategoryResponse)
async def get_subcategory(subcategory_id: int, service: SubCategoryService = Depends(get_subcategory_service)):
    return await service.get_by_id(subcategory_id)

@router.post("", response_model=SubCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_subcategory(
    data: SubCategoryCreate,
    service: SubCategoryService = Depends(get_subcategory_service),
    _ = Depends(get_current_admin)
):
    return await service.create(data.title, data.category_id, data.description)

@router.patch("/{subcategory_id}", response_model=SubCategoryResponse)
async def update_subcategory(
    subcategory_id: int,
    data: SubCategoryUpdate,
    service: SubCategoryService = Depends(get_subcategory_service),
    _ = Depends(get_current_admin)
):
    return await service.update(subcategory_id, data.title, data.category_id, data.description)

@router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subcategory(
    subcategory_id: int,
    service: SubCategoryService = Depends(get_subcategory_service),
    _ = Depends(get_current_admin)
):
    await service.delete(subcategory_id)