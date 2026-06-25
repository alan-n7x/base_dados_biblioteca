from pydantic import BaseModel
from typing import Optional, List

class AuthorBase(BaseModel):
    name: str
    code: str  # codigo do autor

    class Config:
        from_attributes = True

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    name: Optional[str] = None
    code: Optional[str] = None

class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class Author(AuthorInDBBase):
    pass

class AuthorWithBooks(AuthorInDBBase):
    books: list = []

    class Config:
        from_attributes = True

# Avoid circular import by using forward references
from .book import Book, BookInDBBase

AuthorWithBooks.model_rebuild()