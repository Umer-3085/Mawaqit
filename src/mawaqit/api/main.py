from fastapi import APIRouter
from mawaqit.api.admin.router import router as admin_router
from mawaqit.api.category import category_router
from mawaqit.api.subcategory import subcategory_router
from mawaqit.api.article_videos import article_video_router

api_router = APIRouter(prefix="/api")

api_router.include_router(admin_router)

api_router.include_router(category_router)

api_router.include_router(subcategory_router)

api_router.include_router(article_video_router)