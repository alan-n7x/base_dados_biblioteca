from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import library as crud
from app.schemas import library as schemas
from app.models import associate as associate_model
from app.models import book as book_model
from typing import Optional




router = APIRouter()

@router.post("/", response_model=schemas.Library, status_code=status.HTTP_201_CREATED)
def create_library(library: schemas.LibraryCreate, db: Session = Depends(get_db)):
    db_library = crud.get_library_by_name(db, name=library.name)
    if db_library:
        raise HTTPException(status_code=400, detail="Library with this name already exists")
    return crud.create_library(db=db, library=library)

@router.get("/{library_id}", response_model=schemas.Library)
def read_library(library_id: int, db: Session = Depends(get_db)):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library

@router.get("/", response_model=list[schemas.Library])
def read_libraries(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    address: Optional[str] = None,
    db: Session = Depends(get_db)
):
    libraries = crud.get_libraries(
        db,
        skip=skip,
        limit=limit,
        name=name,
        address=address
    )
    return libraries

@router.patch("/{library_id}", response_model=schemas.Library)
def update_library(library_id: int, library: schemas.LibraryUpdate, db: Session = Depends(get_db)):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return crud.update_library(db=db, library_id=library_id, library=library)

@router.delete("/{library_id}", response_model=schemas.Library)
def delete_library(library_id: int, db: Session = Depends(get_db)):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return crud.delete_library(db=db, library_id=library_id)

# Get associates for a library
@router.get("/{library_id}/associates", response_model=list[schemas.Associate])
def read_library_associates(library_id: int, db: Session = Depends(get_db)):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library.associates

# Get books for a library
@router.get("/{library_id}/books", response_model=list[schemas.Book])
def read_library_books(
    library_id: int,
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    isbn: Optional[str] = None,
    author_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    available: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    books = crud.get_books(
        db,
        skip=skip,
        limit=limit,
        title=title,
        isbn=isbn,
        author_id=author_id,
        subject_id=subject_id,
        available=available,
        library_id=library_id
    )
    return books

# Get detailed library with associates and books
@router.get("/{library_id}/details", response_model=schemas.LibraryWithAssociatesAndBooks)
def read_library_details(library_id: int, db: Session = Depends(get_db)):
    db_library = crud.get_library(db, library_id=library_id)
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library


