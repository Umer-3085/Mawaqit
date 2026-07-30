from pydantic import BaseModel
from typing import Optional, Literal


class TranslationTafseerDetailResponse(BaseModel):
    id: int
    title: str
    lang: str
    author: str
    direction: Optional[Literal["ltr", "rtl"]] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TranslationTafseerDetailSimple(BaseModel):
    id: int
    title: str
    lang: str

    class Config:
        from_attributes = True


class TranslationTafseerDetailList(BaseModel):
    items: list[TranslationTafseerDetailResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
