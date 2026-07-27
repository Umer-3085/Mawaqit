from sqlalchemy import Column, Text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, BIGINT
from mawaqit.database import Base

class VerseText(Base):
    __tablename__ = "verse_texts"
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["surah_number", "verse_number"],
            ["verse.surah_number", "verse.number_in_surah"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )
    
    surah_number = Column(
        TINYINT(unsigned=True),
        primary_key=True,
        nullable=False
    )
    verse_number = Column(
        INTEGER(unsigned=True),
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