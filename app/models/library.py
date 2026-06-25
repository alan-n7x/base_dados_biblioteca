from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from .associate import associate_library

class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)

    # Relationships
    associates = relationship("Associate", secondary=associate_library, back_populates="libraries", cascade="all, delete")
    books = relationship("Book", back_populates="library")