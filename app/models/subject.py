from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

# Association table for book and subject
book_subject = Table(
    "book_subject",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("subject_id", Integer, ForeignKey("subjects.id")),
)

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # codigo do assunto
    description = Column(String)

    # Relationships
    books = relationship("Book", secondary=book_subject, back_populates="subjects")