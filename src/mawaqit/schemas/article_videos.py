from pydantic import BaseModel, Field
from typing import Optional

class ArticleVideoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    detail: Optional[str] = None
    category_id: int
    subcategory_id: Optional[int] = None
    link: Optional[str] = Field(None, max_length=1000)

class ArticleVideoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    detail: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    link: Optional[str] = Field(None, max_length=1000)

class ArticleVideoResponse(BaseModel):
    id: int
    title: str
    detail: Optional[str] = None
    category_id: int
    subcategory_id: Optional[int] = None
    link: Optional[str] = None
    content_type: str  # "article" or "video" - computed
    class Config:
        from_attributes = True

class ArticleVideoList(BaseModel):
    items: list[ArticleVideoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int