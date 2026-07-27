from fastapi import APIRouter, Depends, Query
from mawaqit.schemas.verse_texts import VerseTextResponse, VerseTextList
from mawaqit.services.verse_texts import VerseTextService
from mawaqit.api.deps import get_verse_texts_service

router = APIRouter(prefix="/verse-texts", tags=["Verse Texts"])

@router.get("", response_model=VerseTextList)
async def list_verse_texts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    surah_number: int | None = Query(None, ge=1, le=114),
    verse_number: int | None = Query(None, ge=1),
    detail_id: int | None = Query(None, ge=1),
    lang: str | None = Query(None, min_length=2, max_length=2),
    has_tafseer: bool | None = Query(None),
    search: str | None = Query(None, max_length=200),
    service: VerseTextService = Depends(get_verse_texts_service)
):
    filters = {k: v for k, v in locals().items() 
               if k not in ("page", "page_size", "service") and v is not None}
    items, total = await service.get_all(page, page_size, **filters)
    total_pages = (total + page_size - 1) // page_size
    return VerseTextList(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)

@router.get("/surah/{surah_number}", response_model=VerseTextList)
async def get_verse_texts_by_surah(
    surah_number: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: VerseTextService = Depends(get_verse_texts_service)
):
    items, total = await service.get_by_surah(surah_number, page, page_size)
    total_pages = (total + page_size - 1) // page_size
    return VerseTextList(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)

@router.get("/surah/{surah_number}/{verse_number}", response_model=list[VerseTextResponse])
async def get_verse_texts_by_verse(
    surah_number: int,
    verse_number: int,
    service: VerseTextService = Depends(get_verse_texts_service)
):
    return await service.get_by_verse(surah_number, verse_number)

@router.get("/by-detail/{detail_id}", response_model=VerseTextList)
async def get_verse_texts_by_detail(
    detail_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: VerseTextService = Depends(get_verse_texts_service)
):
    items, total = await service.get_by_detail(detail_id, page, page_size)
    total_pages = (total + page_size - 1) // page_size
    return VerseTextList(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)

@router.get("/by-lang/{lang}", response_model=VerseTextList)
async def get_verse_texts_by_lang(
    lang: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: VerseTextService = Depends(get_verse_texts_service)
):
    items, total = await service.get_by_lang(lang, page, page_size)
    total_pages = (total + page_size - 1) // page_size
    return VerseTextList(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)

@router.get("/{surah_number}/{verse_number}/{detail_id}", response_model=VerseTextResponse)
async def get_verse_text(
    surah_number: int,
    verse_number: int,
    detail_id: int,
    service: VerseTextService = Depends(get_verse_texts_service)
):
    return await service.get_by_composite_key(surah_number, verse_number, detail_id)