from pydantic import BaseModel, Field
from typing import Optional, Literal

class VerseResponse(BaseModel):
    surah_number: int
    number_in_surah: int
    arabic: Optional[str] = None
    global_number: int
    juz: Optional[int] = None
    manzil: Optional[int] = None
    page_no: Optional[int] = None
    ruku: Optional[int] = None
    hizb_quarter: Optional[int] = None
    sajda: bool
    class Config:
        from_attributes = True

class VerseList(BaseModel):
    items: list[VerseResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
