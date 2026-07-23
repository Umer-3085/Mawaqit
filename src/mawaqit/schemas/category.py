from pydantic import BaseModel, Field
from typing import Optional

class CategoryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

class CategoryList(BaseModel):
    items: list[CategoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int