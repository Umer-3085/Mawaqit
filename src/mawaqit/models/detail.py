from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.dialects.mysql import BIGINT, CHAR
from mawaqit.database import Base

class TranslationTafseerDetail(Base):
    __tablename__ = "translation_tafseer_details"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    lang = Column(CHAR(2), nullable=False)
    author = Column(String(100), nullable=False)
    direction = Column(Enum('ltr', 'rtl', name='direction_enum'), nullable=True)
    description = Column(Text, nullable=True)