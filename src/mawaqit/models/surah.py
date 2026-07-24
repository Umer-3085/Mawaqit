from sqlalchemy import Column, String, SmallInteger, Enum, Text
from sqlalchemy.dialects.mysql import TINYINT
from mawaqit.database import Base

class Surah(Base):
    __tablename__ = "surah"
    surah_number = Column(TINYINT(unsigned=True), primary_key=True, autoincrement=False)
    total_ayat = Column(SmallInteger(unsigned=True), nullable=False)
    name_arabic = Column(String(100), nullable=False, unique=True)
    english_name = Column(String(100), nullable=False)
    english_name_translation = Column(String(100), nullable=False)
    revelation_type = Column(Enum('Meccan', 'Medinan', name='revelation_type'), nullable=False)