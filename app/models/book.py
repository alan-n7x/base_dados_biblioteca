from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    library_id = Column(Integer, ForeignKey("libraries.id"))

    # Relationships
    library = relationship("Library", back_populates="books")
    authors = relationship("Author", secondary="book_author", back_populates="books")
    subjects = relationship("Subject", secondary="book_subject", back_populates="books")
    # A book can have at most one active loan? We'll handle that in the loan model and business logic.
    # For simplicity, we'll have a one-to-many from Book to Loan (historical loans)
    loans = relationship("Loan", back_populates="book")