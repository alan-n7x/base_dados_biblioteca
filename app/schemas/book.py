from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    isbn: str

    class Config:
        from_attributes = True

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    isbn: Optional[str] = None

class BookInDBBase(BookBase):
    id: int

    class Config:
        from_attributes = True

class Book(BookInDBBase):
    pass

class BookWithAuthorsAndSubjects(BookInDBBase):
    authors: list = []
    subjects: list = []

    class Config:
        from_attributes = True

# Avoid circular import by using forward references
from .author import Author, AuthorInDBBase
from .subject import Subject, SubjectInDBBase

BookWithAuthorsAndSubjects.model_rebuild()