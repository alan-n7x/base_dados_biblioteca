from pydantic import BaseModel
from typing import Optional, List

class LibraryBase(BaseModel):
    name: str
    address: str

class LibraryCreate(LibraryBase):
    pass

class LibraryUpdate(LibraryBase):
    name: Optional[str] = None
    address: Optional[str] = None

class LibraryInDBBase(LibraryBase):
    id: int

    class Config:
        from_attributes = True

class Library(LibraryInDBBase):
    pass

class LibraryWithAssociatesAndBooks(LibraryInDBBase):
    associates: list = []
    books: list = []

    class Config:
        from_attributes = True


class LibraryStats(BaseModel):
    books_count: int
    authors_count: int
    associates_count: int
    active_loans: int
    returned_loans: int

    class Config:
        from_attributes = True


# Avoid circular import by using forward references
from .associate import Associate, AssociateInDBBase
from .book import Book, BookInDBBase

LibraryWithAssociatesAndBooks.model_rebuild()