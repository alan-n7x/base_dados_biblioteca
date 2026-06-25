from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoanBase(BaseModel):
    associate_id: int
    book_id: int
    loan_date: Optional[datetime] = None
    return_date: Optional[datetime] = None

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    associate_id: Optional[int] = None
    book_id: Optional[int] = None
    loan_date: Optional[datetime] = None
    return_date: Optional[datetime] = None

class LoanInDBBase(LoanBase):
    id: int

    class Config:
        from_attributes = True

class Loan(LoanInDBBase):
    pass

class LoanWithAssociateAndBook(LoanInDBBase):
    associate: "Associate" = None
    book: "Book" = None

    class Config:
        from_attributes = True

# Avoid circular import by using forward references
from .associate import Associate, AssociateInDBBase
from .book import Book, BookInDBBase

LoanWithAssociateAndBook.model_rebuild()