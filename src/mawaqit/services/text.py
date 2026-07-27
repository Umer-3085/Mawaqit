from fastapi import HTTPException
from mawaqit.repositories.text import VerseTextRepository
from mawaqit.repositories.surah import SurahRepository
from mawaqit.repositories.verse import VerseRepository
from mawaqit.repositories.detail import TranslationTafseerDetailRepository
from mawaqit.models.text import VerseText

class VerseTextService:
    def __init__(
        self, 
        repo: VerseTextRepository,
        surah_repo: SurahRepository,
        verse_repo: VerseRepository,
        detail_repo: TranslationTafseerDetailRepository
    ):
        self.repo = repo
        self.surah_repo = surah_repo
        self.verse_repo = verse_repo
        self.detail_repo = detail_repo

    async def get_by_composite_key(self, surah_number: int, verse_number: int, detail_id: int) -> VerseText:
        if not 1 <= surah_number <= 114:
            raise HTTPException(status_code=400, detail="Surah number must be between 1 and 114")
        if verse_number < 1:
            raise HTTPException(status_code=400, detail="Verse number must be positive")
        if detail_id <= 0:
            raise HTTPException(status_code=400, detail="Detail ID must be positive")
        
        # Validate surah exists
        surah = await self.surah_repo.get_by_number(surah_number)
        if not surah:
            raise HTTPException(status_code=404, detail="Surah not found")
        
        # Validate verse exists
        if verse_number > surah.total_ayat:
            raise HTTPException(status_code=400, detail=f"Verse number must be between 1 and {surah.total_ayat} for this surah")
        
        # Validate detail exists
        detail = await self.detail_repo.get_by_id(detail_id)
        if not detail:
            raise HTTPException(status_code=404, detail="Translation/Tafseer detail not found")
        
        verse_text = await self.repo.get_by_composite_key(surah_number, verse_number, detail_id)
        if not verse_text:
            raise HTTPException(status_code=404, detail="Verse text not found")
        return verse_text

    async def get_all(self, page: int, page_size: int, **filters):
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
        return await self.repo.get_all_with_details(page, page_size, **filters)

    async def get_by_surah(self, surah_number: int, page: int, page_size: int):
        if not 1 <= surah_number <= 114:
            raise HTTPException(status_code=400, detail="Surah number must be between 1 and 114")
        surah = await self.surah_repo.get_by_number(surah_number)
        if not surah:
            raise HTTPException(status_code=404, detail="Surah not found")
        return await self.repo.get_by_surah(surah_number, page, page_size)

    async def get_by_verse(self, surah_number: int, verse_number: int):
        if not 1 <= surah_number <= 114:
            raise HTTPException(status_code=400, detail="Surah number must be between 1 and 114")
        surah = await self.surah_repo.get_by_number(surah_number)
        if not surah:
            raise HTTPException(status_code=404, detail="Surah not found")
        if not 1 <= verse_number <= surah.total_ayat:
            raise HTTPException(status_code=400, detail=f"Verse number must be between 1 and {surah.total_ayat} for this surah")
        return await self.repo.get_by_verse(surah_number, verse_number)

    async def get_by_detail(self, detail_id: int, page: int, page_size: int):
        if detail_id <= 0:
            raise HTTPException(status_code=400, detail="Detail ID must be positive")
        detail = await self.detail_repo.get_by_id(detail_id)
        if not detail:
            raise HTTPException(status_code=404, detail="Translation/Tafseer detail not found")
        return await self.repo.get_by_detail(detail_id, page, page_size)

    async def get_by_lang(self, lang: str, page: int, page_size: int):
        if not lang or len(lang) != 2:
            raise HTTPException(status_code=400, detail="Language code must be 2 characters")
        return await self.repo.get_by_lang(lang, page, page_size)