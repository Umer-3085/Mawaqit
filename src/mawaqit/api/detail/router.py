from fastapi import APIRouter, Depends, Query, Path
from mawaqit.schemas.detail import (
    TranslationTafseerDetailResponse,
    TranslationTafseerDetailSimple,
    TranslationTafseerDetailList,
)
from mawaqit.services.detail import TranslationTafseerDetailService
from mawaqit.api.deps import get_translation_tafseer_details_service

router = APIRouter(prefix="/translation-tafseer-details", tags=["Translation/Tafseer Details"])


@router.get("", response_model=TranslationTafseerDetailList)
async def list_details(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    lang: str | None = Query(None, min_length=2, max_length=2),
    direction: str | None = Query(None, pattern="^(ltr|rtl)$"),
    author: str | None = Query(None, max_length=100),
    search: str | None = Query(None, max_length=200),
    service: TranslationTafseerDetailService = Depends(get_translation_tafseer_details_service),
):
    items, total = await service.get_all(page, page_size, lang, direction, author, search)
    total_pages = (total + page_size - 1) // page_size
    return TranslationTafseerDetailList(
        items=items, total=total, page=page, page_size=page_size, total_pages=total_pages
    )


@router.get("/all", response_model=list[TranslationTafseerDetailSimple])
async def list_all_simple(
    service: TranslationTafseerDetailService = Depends(get_translation_tafseer_details_service),
):
    return await service.get_all_simple()


@router.get("/{id}", response_model=TranslationTafseerDetailResponse)
async def get_detail(
    id: int,
    service: TranslationTafseerDetailService = Depends(get_translation_tafseer_details_service),
):
    return await service.get_by_id(id)


@router.get("/by-lang/{lang}", response_model=list[TranslationTafseerDetailResponse])
async def get_by_lang(
    lang: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    service: TranslationTafseerDetailService = Depends(get_translation_tafseer_details_service),
):
    return await service.get_by_lang(lang, page, page_size)


@router.get("/by-direction/{direction}", response_model=list[TranslationTafseerDetailResponse])
async def get_by_direction(
    direction: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    service: TranslationTafseerDetailService = Depends(get_translation_tafseer_details_service),
):
    return await service.get_by_direction(direction, page, page_size)


@router.get("/by-author/{author}", response_model=list[TranslationTafseerDetailResponse])
async def get_by_author(
    author: str = Path(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    service: TranslationTafseerDetailService = Depends(get_translation_tafseer_details_service),
):
    return await service.get_by_author(author, page, page_size)
