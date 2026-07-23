from pydantic import BaseModel, Field
from typing import Optional

class SubCategoryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    category_id: int
    description: Optional[str] = None

class SubCategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    category_id: Optional[int] = None
    description: Optional[str] = None

class SubCategoryResponse(BaseModel):
    id: int
    title: str
    category_id: int
    description: Optional[str] = None
    class Config:
        from_attributes = True

class SubCategoryList(BaseModel):
    items: list[SubCategoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    