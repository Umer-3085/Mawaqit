from fastapi import APIRouter, Depends, Query, Path
from mawaqit.schemas.verse import VerseResponse, VerseList
from mawaqit.services.verse import VerseService
from mawaqit.api.deps import get_verse_service

router = APIRouter(prefix="/verses", tags=["Verses"])

@router.get("", response_model=VerseList)
async def list_verses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    surah_number: int | None = Query(None, ge=1, le=114),
    juz: int | None = Query(None, ge=1, le=30),
    manzil: int | None = Query(None, ge=1, le=7),
    page_no: int | None = Query(None, ge=1),
    ruku: int | None = Query(None, ge=1),
    hizb_quarter: int | None = Query(None, ge=1, le=240),
    sajda: bool | None = Query(None),
    search: str | None = Query(None, max_length=200),
    service: VerseService = Depends(get_verse_service)
):
    filters = {k: v for k, v in locals().items() 
               if k not in ("page", "page_size", "service") and v is not None}
    items, total = await service.get_all(page, page_size, **filters)
    total_pages = (total + page_size - 1) // page_size
    return VerseList(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)

@router.get("/global/{global_number}", response_model=VerseResponse)
async def get_verse_by_global(global_number: int, service: VerseService = Depends(get_verse_service)):
    return await service.get_by_global_number(global_number)

@router.get("/surah/{surah_number}", response_model=list[VerseResponse])
async def get_verses_by_surah(surah_number: int = Path(..., ge=1, le=114), service: VerseService = Depends(get_verse_service)):
    return await service.get_by_surah(surah_number)

@router.get("/surah/{surah_number}/{number_in_surah}", response_model=VerseResponse)
async def get_verse(surah_number: int = Path(..., ge=1, le=114), number_in_surah: int = Path(..., ge=1), service: VerseService = Depends(get_verse_service)):
    return await service.get_by_composite_key(surah_number, number_in_surah)

@router.get("/by-juz/{juz}", response_model=list[VerseResponse])
async def get_verses_by_juz(juz: int = Path(..., ge=1, le=30), service: VerseService = Depends(get_verse_service)):
    items, _ = await service.repo.get_all(page=1, page_size=6000, juz=juz)  # ~6000 verses max
    return items

@router.get("/by-page/{page_no}", response_model=list[VerseResponse])
async def get_verses_by_page(page_no: int = Path(..., ge=1), service: VerseService = Depends(get_verse_service)):
    items, _ = await service.repo.get_all(page=1, page_size=6000, page_no=page_no)
    return items

@router.get("/sajda", response_model=list[VerseResponse])
async def get_sajda_verses(service: VerseService = Depends(get_verse_service)):
    items, _ = await service.repo.get_all(page=1, page_size=6000, sajda=True)
    return items
