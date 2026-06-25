from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import author as crud
from app.schemas import author as schemas
from app.models import book as book_model

router = APIRouter()

@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_code(db, code=author.code)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with this code already exists")
    return crud.create_author(db=db, author=author)

@router.get("/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.get("/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    authors = crud.get_authors(
        db,
        skip=skip,
        limit=limit,
        name=name,
        code=code
    )
    return authors

@router.patch("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.update_author(db=db, author_id=author_id, author=author)

@router.delete("/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.delete_author(db=db, author_id=author_id)

# Get books for an author
@router.get("/{author_id}/books", response_model=list[schemas.Book])
def read_author_books(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author.books