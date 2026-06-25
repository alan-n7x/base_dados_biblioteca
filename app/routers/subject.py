from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import subject as crud
from app.schemas import subject as schemas
from app.models import book as book_model
from typing import Optional

router = APIRouter()

@router.post("/", response_model=schemas.Subject, status_code=status.HTTP_201_CREATED)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_subject = crud.get_subject_by_code(db, code=subject.code)
    if db_subject:
        raise HTTPException(status_code=400, detail="Subject with this code already exists")
    return crud.create_subject(db=db, subject=subject)

@router.get("/{subject_id}", response_model=schemas.Subject)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@router.get("/", response_model=list[schemas.Subject])
def read_subjects(
    skip: int = 0,
    limit: int = 100,
    description: Optional[str] = None,
    code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    subjects = crud.get_subjects(
        db,
        skip=skip,
        limit=limit,
        description=description,
        code=code
    )
    return subjects

@router.patch("/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: int, subject: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return crud.update_subject(db=db, subject_id=subject_id, subject=subject)

@router.delete("/{subject_id}", response_model=schemas.Subject)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return crud.delete_subject(db=db, subject_id=subject_id)

# Get books for a subject
@router.get("/{subject_id}/books", response_model=list[schemas.Book])
def read_subject_books(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id=subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject.books