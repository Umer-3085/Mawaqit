from sqlalchemy import Column, String
from mawaqit.database import Base

class Admin(Base):
    __tablename__ = "admin"
    username = Column(String(100), primary_key=True, unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)