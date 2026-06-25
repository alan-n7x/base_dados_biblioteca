from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import library as models
from app.schemas import library as schemas
from app.models import associate as associate_model
from app.models import book as book_model
from app.models import loan as loan_model
from app.models import author as author_model
from typing import Optional

def get_library(db: Session, library_id: int):
    return db.query(models.Library).filter(models.Library.id == library_id).first()

def get_library_by_name(db: Session, name: str):
    return db.query(models.Library).filter(models.Library.name == name).first()

def get_libraries(db: Session, skip: int = 0, limit: int = 100, name: Optional[str] = None, address: Optional[str] = None):
    query = db.query(models.Library)
    if name:
        query = query.filter(models.Library.name.ilike(f"%{name}%"))
    if address:
        query = query.filter(models.Library.address.ilike(f"%{address}%"))
    return query.offset(skip).limit(limit).all()


def get_library_stats(db: Session, library_id: int):
    # Get counts for a specific library
    books_count = db.query(func.count(book_model.Book.id)).filter(book_model.Book.library_id == library_id).scalar()
    authors_count = db.query(func.count(author_model.Author.id)).join(book_model.Book.authors).join(book_model.Book).filter(book_model.Book.library_id == library_id).scalar()
    # Associates count via many-to-many
    associates_count = (
        db.query(func.count(associate_model.Associate.id))
        .join(associate_model.Associate.libraries)
        .filter(models.Library.id == library_id)
        .scalar()
    )

    # Active loans (books currently checked out from this library)
    active_loans = db.query(func.count(loan_model.Loan.id)).join(book_model.Book).filter(
        book_model.Book.library_id == library_id,
        loan_model.Loan.return_date == None
    ).scalar()

    # Returned loans (books that were checked out and returned from this library)
    returned_loans = db.query(func.count(loan_model.Loan.id)).join(book_model.Book).filter(
        book_model.Book.library_id == library_id,
        loan_model.Loan.return_date != None
    ).scalar()

    return schemas.LibraryStats(
        books_count=books_count,
        authors_count=authors_count,
        associates_count=associates_count,
        active_loans=active_loans,
        returned_loans=returned_loans
    )

def create_library(db: Session, library: schemas.LibraryCreate):
    db_library = models.Library(
        name=library.name,
        address=library.address
    )
    db.add(db_library)
    db.commit()
    db.refresh(db_library)
    return db_library

def update_library(db: Session, library_id: int, library: schemas.LibraryUpdate):
    db_library = db.query(models.Library).filter(models.Library.id == library_id).first()
    if db_library:
        update_data = library.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_library, field, value)
        db.commit()
        db.refresh(db_library)
    return db_library

def delete_library(db: Session, library_id: int):
    db_library = db.query(models.Library).filter(models.Library.id == library_id).first()
    if db_library:
        db.delete(db_library)
        db.commit()
    return db_library