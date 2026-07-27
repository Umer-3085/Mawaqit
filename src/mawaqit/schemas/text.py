from pydantic import BaseModel
from typing import Optional

class VerseTextResponse(BaseModel):
    surah_number: int
    verse_number: int
    detail_id: int
    verse_translation: str
    verse_tafseer: Optional[str] = None
    class Config:
        from_attributes = True

class VerseTextList(BaseModel):
    items: list[VerseTextResponse]
    total: int
    page: int
    page_size: int
    total_pages: int