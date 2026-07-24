from fastapi import APIRouter, Depends, Query
from mawaqit.schemas.surah import SurahResponse, SurahList
from mawaqit.services.surah import SurahService
from mawaqit.api.deps import get_surah_service

router = APIRouter(prefix="/surahs", tags=["Surahs"])

@router.get("", response_model=SurahList)
async def list_surahs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    revelation_type: str | None = Query(None, pattern="^(Meccan|Medinan|all)$"),
    search: str | None = Query(None, max_length=100),
    service: SurahService = Depends(get_surah_service)
):
    items, total = await service.get_all(page, page_size, revelation_type, search)
    total_pages = (total + page_size - 1) // page_size
    return SurahList(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)

@router.get("/all", response_model=list[SurahResponse])
async def list_all_surahs(service: SurahService = Depends(get_surah_service)):
    """Lightweight list of all 114 surahs for dropdowns"""
    return await service.get_all_simple()

@router.get("/{surah_number}", response_model=SurahResponse)
async def get_surah(surah_number: int, service: SurahService = Depends(get_surah_service)):
    return await service.get_by_number(surah_number)

@router.get("/by-revelation/{revelation_type}", response_model=list[SurahResponse])
async def get_surahs_by_revelation(revelation_type: str, service: SurahService = Depends(get_surah_service)):
    return await service.get_by_revelation_type(revelation_type)

@router.get("/search", response_model=list[SurahResponse])
async def search_surahs(q: str = Query(..., min_length=1, max_length=100), service: SurahService = Depends(get_surah_service)):
    items, _ = await service.repo.get_all(page=1, page_size=114, search=q)
    return items
