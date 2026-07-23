from fastapi import APIRouter, Depends, status, Query
from typing import Literal
from mawaqit.schemas.article_videos import (
    ArticleVideoCreate, ArticleVideoUpdate, ArticleVideoResponse, ArticleVideoList
)
from mawaqit.services.article_videos import ArticleVideoService
from mawaqit.api.deps import get_article_video_service, get_current_admin

router = APIRouter(prefix="/articles-videos", tags=["Articles/Videos"])

@router.get("", response_model=ArticleVideoList)
async def list_articles_videos(
    page: int = 1,
    page_size: int = 20,
    category_id: int | None = None,
    subcategory_id: int | None = None,
    type: Literal["all", "video", "article"] = "all",
    service: ArticleVideoService = Depends(get_article_video_service)
):
    items, total = await service.get_all(page, page_size, category_id, subcategory_id, type)
    total_pages = (total + page_size - 1) // page_size
    return ArticleVideoList(
        items=items, total=total, page=page, page_size=page_size, total_pages=total_pages
    )

@router.get("/{id}", response_model=ArticleVideoResponse)
async def get_article_video(id: int, service: ArticleVideoService = Depends(get_article_video_service)):
    return await service.get_by_id(id)

@router.post("", response_model=ArticleVideoResponse, status_code=status.HTTP_201_CREATED)
async def create_article_video(
    data: ArticleVideoCreate,
    service: ArticleVideoService = Depends(get_article_video_service),
    _ = Depends(get_current_admin)
):
    return await service.create(data.title, data.category_id, data.detail, data.subcategory_id, data.link)

@router.patch("/{id}", response_model=ArticleVideoResponse)
async def update_article_video(
    id: int,
    data: ArticleVideoUpdate,
    service: ArticleVideoService = Depends(get_article_video_service),
    _ = Depends(get_current_admin)
):
    return await service.update(id, data.title, data.detail, data.category_id, data.subcategory_id, data.link)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_video(
    id: int,
    service: ArticleVideoService = Depends(get_article_video_service),
    _ = Depends(get_current_admin)
):
    await service.delete(id)