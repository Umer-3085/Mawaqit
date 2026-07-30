from sqlalchemy import Column, String, Text, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, INTEGER
from mawaqit.database import Base


class Verse(Base):
    __tablename__ = "verse"

    # Composite Primary Key
    surah_number = Column(
        TINYINT(unsigned=True),
        ForeignKey("surah.surah_number", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    number_in_surah = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)

    arabic = Column(Text, nullable=True)
    global_number = Column(INTEGER(unsigned=True), unique=True, nullable=False)
    juz = Column(TINYINT(unsigned=True), nullable=True)
    manzil = Column(TINYINT(unsigned=True), nullable=True)
    page_no = Column(SMALLINT(unsigned=True), nullable=True)
    ruku = Column(SMALLINT(unsigned=True), nullable=True)
    hizb_quarter = Column(TINYINT(unsigned=True), nullable=True)
    sajda = Column(Boolean, default=False, nullable=False)
