from sqlalchemy import Column, BigInteger, String, Text, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from mawaqit.database import Base

class ArticleVideo(Base):
    __tablename__ = "article_videos"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    detail = Column(Text, nullable=True)
    category_id = Column(BigInteger, ForeignKey("category.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    subcategory_id = Column(BigInteger, ForeignKey("subcategory.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    link = Column(String(1000), nullable=True)

    @hybrid_property
    def content_type(self) -> str:
        return "video" if self.link else "article"