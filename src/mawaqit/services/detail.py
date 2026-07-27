from fastapi import HTTPException
from mawaqit.repositories.translation_tafseer_details import TranslationTafseerDetailRepository
from mawaqit.models.translation_tafseer_details import TranslationTafseerDetail

class TranslationTafseerDetailService:
    def __init__(self, repo: TranslationTafseerDetailRepository):
        self.repo = repo

    async def get_by_id(self, id: int) -> TranslationTafseerDetail:
        if id <= 0:
            raise HTTPException(status_code=400, detail="ID must be positive")
        detail = await self.repo.get_by_id(id)
        if not detail:
            raise HTTPException(status_code=404, detail="Translation/Tafseer detail not found")
        return detail

    async def get_all(self, page: int, page_size: int, lang: str | None, direction: str | None, author: str | None, search: str | None):
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
        if direction and direction not in ("ltr", "rtl"):
            raise HTTPException(status_code=400, detail="Direction must be 'ltr' or 'rtl'")
        return await self.repo.get_all(page, page_size, lang, direction, author, search)

    async def get_all_simple(self) -> list[TranslationTafseerDetail]:
        return await self.repo.get_all_simple()

    async def get_by_lang(self, lang: str, page: int, page_size: int) -> list[TranslationTafseerDetail]:
        if not lang or len(lang) != 2:
            raise HTTPException(status_code=400, detail="Language code must be 2 characters")
        items, _ = await self.repo.get_by_lang(lang, page, page_size)
        return items

    async def get_by_direction(self, direction: str, page: int, page_size: int) -> list[TranslationTafseerDetail]:
        if direction not in ("ltr", "rtl"):
            raise HTTPException(status_code=400, detail="Direction must be 'ltr' or 'rtl'")
        items, _ = await self.repo.get_by_direction(direction, page, page_size)
        return items

    async def get_by_author(self, author: str, page: int, page_size: int) -> list[TranslationTafseerDetail]:
        if not author or len(author.strip()) == 0:
            raise HTTPException(status_code=400, detail="Author name required")
        items, _ = await self.repo.get_by_author(author.strip(), page, page_size)
        return items