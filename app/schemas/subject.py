from pydantic import BaseModel
from typing import Optional, List

class SubjectBase(BaseModel):
    description: str
    code: str  # codigo do assunto

    class Config:
        from_attributes = True

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    description: Optional[str] = None
    code: Optional[str] = None

class SubjectInDBBase(SubjectBase):
    id: int

    class Config:
        from_attributes = True

class Subject(SubjectInDBBase):
    pass

class SubjectWithBooks(SubjectInDBBase):
    books: list = []

    class Config:
        from_attributes = True

# Avoid circular import by using forward references
from .book import Book, BookInDBBase

SubjectWithBooks.model_rebuild()