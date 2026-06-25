from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import book as models
from app.models import author as author_model
from app.models import subject as subject_model
from app.models import loan as loan_model
from app.schemas import book as schemas
from typing import Optional

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_isbn(db: Session, isbn: str):
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def get_books(db: Session, skip: int = 0, limit: int = 100, title: Optional[str] = None, isbn: Optional[str] = None, author_id: Optional[int] = None, subject_id: Optional[int] = None, available: Optional[bool] = None, library_id: Optional[int] = None):
    query = db.query(models.Book)

    if library_id is not None:
        query = query.filter(models.Book.library_id == library_id)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if isbn:
        query = query.filter(models.Book.isbn == isbn)
    if author_id is not None:
        query = query.join(models.Book.authors).filter(models.Author.id == author_id)
    if subject_id is not None:
        query = query.join(models.Book.subjects).filter(models.Subject.id == subject_id)
    if available is not None:
        # Subquery to count active loans per book
        active_loans_subq = db.query(loan_model.Loan.book_id, func.count(loan_model.Loan.id).label('active_count')) \
            .filter(loan_model.Loan.return_date == None) \
            .group_by(loan_model.Loan.book_id).subquery()
        if available:
            # books with zero active loans: left join and where active_count is null or 0
            query = query.outerjoin(active_loans_subq, models.Book.id == active_loans_subq.c.book_id) \
                .filter((active_loans_subq.c.active_count == None) | (active_loans_subq.c.active_count == 0))
        else:
            # books with at least one active loan
            query = query.join(active_loans_subq, models.Book.id == active_loans_subq.c.book_id) \
                .filter(active_loans_subq.c.active_count > 0)

    return query.offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        isbn=book.isbn,
        title=book.title
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        update_data = book.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

# Helper functions to manage many-to-many relationships
def add_author_to_book(db: Session, book_id: int, author_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_author = db.query(author_model.Author).filter(author_model.Author.id == author_id).first()
    if db_book and db_author:
        if db_author not in db_book.authors:
            db_book.authors.append(db_author)
            db.commit()
            db.refresh(db_book)
    return db_book

def remove_author_from_book(db: Session, book_id: int, author_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_author = db.query(author_model.Author).filter(author_model.Author.id == author_id).first()
    if db_book and db_author:
        if db_author in db_book.authors:
            db_book.authors.remove(db_author)
            db.commit()
            db.refresh(db_book)
    return db_book

def add_subject_to_book(db: Session, book_id: int, subject_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_subject = db.query(subject_model.Subject).filter(subject_model.Subject.id == subject_id).first()
    if db_book and db_subject:
        if db_subject not in db_book.subjects:
            db_book.subjects.append(db_subject)
            db.commit()
            db.refresh(db_book)
    return db_book

def remove_subject_from_book(db: Session, book_id: int, subject_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_subject = db.query(subject_model.Subject).filter(subject_model.Subject.id == subject_id).first()
    if db_book and db_subject:
        if db_subject in db_book.subjects:
            db_book.subjects.remove(db_subject)
            db.commit()
            db.refresh(db_book)
    return db_book