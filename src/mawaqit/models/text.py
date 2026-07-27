from sqlalchemy import Column, Text, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, BIGINT
from mawaqit.database import Base

class VerseText(Base):
    __tablename__ = "verse_texts"
    
    surah_number = Column(
        TINYINT(unsigned=True),
        ForeignKey("verse.surah_number", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False
    )
    verse_number = Column(
        INTEGER(unsigned=True),
        ForeignKey("verse.number_in_surah", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False
    )
    detail_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("translation_tafseer_details.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False
    )
    verse_translation = Column(Text, nullable=False)
    verse_tafseer = Column(Text, nullable=True)