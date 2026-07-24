from fastapi import HTTPException
from mawaqit.repositories.surah import SurahRepository
from mawaqit.models.surah import Surah

class SurahService:
    def __init__(self, repo: SurahRepository):
        self.repo = repo

    async def get_by_number(self, surah_number: int) -> Surah:
        if not 1 <= surah_number <= 114:
            raise HTTPException(status_code=400, detail="Surah number must be between 1 and 114")
        surah = await self.repo.get_by_number(surah_number)
        if not surah:
            raise HTTPException(status_code=404, detail="Surah not found")
        return surah

    async def get_all(self, page: int, page_size: int, revelation_type: str | None, search: str | None):
        return await self.repo.get_all(page, page_size, revelation_type, search)

    async def get_all_simple(self) -> list[Surah]:
        return await self.repo.get_all_simple()

    async def get_by_revelation_type(self, revelation_type: str) -> list[Surah]:
        if revelation_type not in ("Meccan", "Medinan"):
            raise HTTPException(status_code=400, detail="Revelation type must be 'Meccan' or 'Medinan'")
        # Reuse get_all with page_size=114 (max surahs)
        items, _ = await self.repo.get_all(page=1, page_size=114, revelation_type=revelation_type)
        return items
