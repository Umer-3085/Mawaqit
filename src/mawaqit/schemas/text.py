from pydantic import BaseModel, Field
from typing import Optional
from mawaqit.schemas.detail import TranslationTafseerDetailResponse

class VerseTextResponse(BaseModel):
    surah_number: int
    verse_number: int
    detail_id: int
    verse_translation: str
    verse_tafseer: Optional[str] = None
    translation_detail: Optional[TranslationTafseerDetailResponse] = None
    class Config:
        from_attributes = True

class VerseTextList(BaseModel):
    items: list[VerseTextResponse]
    total: int
    page: int
    page_size: int
    total_pages: int