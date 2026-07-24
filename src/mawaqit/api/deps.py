from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from mawaqit.database import get_db
from mawaqit.config import settings
from mawaqit.repositories.admin import AdminRepository
from mawaqit.services.admin import AdminService
from mawaqit.models.admin import Admin

from mawaqit.repositories.category import CategoryRepository
from mawaqit.services.category import CategoryService

from mawaqit.repositories.subcategory import SubCategoryRepository
from mawaqit.services.subcategory import SubCategoryService
from mawaqit.repositories.category import CategoryRepository

from mawaqit.repositories.article_videos import ArticleVideoRepository
from mawaqit.services.article_videos import ArticleVideoService
from mawaqit.repositories.category import CategoryRepository
from mawaqit.repositories.subcategory import SubCategoryRepository

from mawaqit.repositories.surah import SurahRepository
from mawaqit.services.surah import SurahService

oauth2_scheme = HTTPBearer(auto_error=False)

async def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(AdminRepository(db))

async def get_current_admin(
    credentials = Depends(oauth2_scheme),
    service: AdminService = Depends(get_admin_service)
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admin = await service.repo.get_by_username(username)
    if admin is None:
        raise credentials_exception
    return admin

async def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))

async def get_subcategory_service(db: AsyncSession = Depends(get_db)) -> SubCategoryService:
    return SubCategoryService(SubCategoryRepository(db), CategoryRepository(db))

async def get_article_video_service(db: AsyncSession = Depends(get_db)) -> ArticleVideoService:
    return ArticleVideoService(
        ArticleVideoRepository(db),
        CategoryRepository(db),
        SubCategoryRepository(db)
    )

async def get_surah_service(db: AsyncSession = Depends(get_db)) -> SurahService:
    return SurahService(SurahRepository(db))