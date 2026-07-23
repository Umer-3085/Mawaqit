from sqlalchemy import Column, BigInteger, String, Text, ForeignKey
from mawaqit.database import Base

class SubCategory(Base):
    __tablename__ = "subcategory"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    category_id = Column(BigInteger, ForeignKey("category.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    description = Column(Text, nullable=True)