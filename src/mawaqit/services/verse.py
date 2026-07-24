from fastapi import HTTPException
from mawaqit.repositories.verse import VerseRepository
from mawaqit.repositories.surah import SurahRepository
from mawaqit.models.verse import Verse

class VerseService:
    def __init__(self, repo: VerseRepository, surah_repo: SurahRepository):
        self.repo = repo
        self.surah_repo = surah_repo

    async def get_by_composite_key(self, surah_number: int, number_in_surah: int) -> Verse:
        if not 1 <= surah_number <= 114:
            raise HTTPException(status_code=400, detail="Surah number must be between 1 and 114")
        
        # Validate surah exists
        surah = await self.surah_repo.get_by_number(surah_number)
        if not surah:
            raise HTTPException(status_code=404, detail="Surah not found")
        
        if not 1 <= number_in_surah <= surah.total_ayat:
            raise HTTPException(
                status_code=400, 
                detail=f"Verse number must be between 1 and {surah.total_ayat} for this surah"
            )
        
        verse = await self.repo.get_by_composite_key(surah_number, number_in_surah)
        if not verse:
            raise HTTPException(status_code=404, detail="Verse not found")
        return verse

    async def get_by_global_number(self, global_number: int) -> Verse:
        verse = await self.repo.get_by_global_number(global_number)
        if not verse:
            raise HTTPException(status_code=404, detail="Verse not found")
        return verse

    async def get_all(self, page: int, page_size: int, **filters):
        return await self.repo.get_all(page, page_size, **filters)

    async def get_by_surah(self, surah_number: int) -> list[Verse]:
        if not 1 <= surah_number <= 114:
            raise HTTPException(status_code=400, detail="Surah number must be between 1 and 114")
        surah = await self.surah_repo.get_by_number(surah_number)
        if not surah:
            raise HTTPException(status_code=404, detail="Surah not found")
        return await self.repo.get_by_surah(surah_number)