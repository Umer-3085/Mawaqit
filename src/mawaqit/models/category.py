from sqlalchemy import Column, BigInteger, String, Text
from mawaqit.database import Base

class Category(Base):
    __tablename__ = "category"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)