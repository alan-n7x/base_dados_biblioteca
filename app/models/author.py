from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

# Association table for book and author
book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # codigo do autor
    name = Column(String, index=True)

    # Relationships
    books = relationship("Book", secondary=book_author, back_populates="authors")