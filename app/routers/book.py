from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import book as crud
from app.schemas import book as schemas
from app.models import author as author_model
from app.models import subject as subject_model
from app.crud import book as book_crud
from typing import Optional

router = APIRouter()

@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_isbn(db, isbn=book.isbn)
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    return crud.create_book(db=db, book=book)

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    isbn: Optional[str] = None,
    author_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    available: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    books = crud.get_books(
        db,
        skip=skip,
        limit=limit,
        title=title,
        isbn=isbn,
        author_id=author_id,
        subject_id=subject_id,
        available=available
    )
    return books

@router.patch("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db=db, book_id=book_id, book=book)

@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.delete_book(db=db, book_id=book_id)

# Author associations
@router.get("/{book_id}/authors", response_model=list[schemas.Author])
def read_book_authors(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book.authors

@router.post("/{book_id}/authors/{author_id}", response_model=schemas.Book)
def add_author_to_book(book_id: int, author_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_author = db.query(author_model.Author).filter(author_model.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    updated_book = book_crud.add_author_to_book(db=db, book_id=book_id, author_id=author_id)
    if updated_book is None:
        raise HTTPException(status_code=400, detail="Failed to associate author with book")
    return updated_book

@router.delete("/{book_id}/authors/{author_id}", response_model=schemas.Book)
def remove_author_from_book(book_id: int, author_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_author = db.query(author_model.Author).filter(author_model.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    updated_book = book_crud.remove_author_from_book(db=db, book_id=book_id, author_id=author_id)
    if updated_book is None:
        raise HTTPException(status_code=400, detail="Failed to remove author from book")
    return updated_book

# Subject associations
@router.get("/{book_id}/subjects", response_model=list[schemas.Subject])
def read_book_subjects(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book.subjects

@router.post("/{book_id}/subjects/{subject_id}", response_model=schemas.Book)
def add_subject_to_book(book_id: int, subject_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_subject = db.query(subject_model.Subject).filter(subject_model.Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    updated_book = book_crud.add_subject_to_book(db=db, book_id=book_id, subject_id=subject_id)
    if updated_book is None:
        raise HTTPException(status_code=400, detail="Failed to associate subject with book")
    return updated_book

@router.delete("/{book_id}/subjects/{subject_id}", response_model=schemas.Book)
def remove_subject_from_book(book_id: int, subject_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_subject = db.query(subject_model.Subject).filter(subject_model.Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    updated_book = book_crud.remove_subject_from_book(db=db, book_id=book_id, subject_id=subject_id)
    if updated_book is None:
        raise HTTPException(status_code=400, detail="Failed to remove subject from book")
    return updated_book