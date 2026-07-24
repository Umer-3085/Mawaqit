from pydantic import BaseModel, Field
from typing import Optional, Literal

class SurahResponse(BaseModel):
    surah_number: int
    total_ayat: int
    name_arabic: str
    english_name: str
    english_name_translation: str
    revelation_type: Literal["Meccan", "Medinan"]
    class Config:
        from_attributes = True

class SurahList(BaseModel):
    items: list[SurahResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
