from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import loan as crud
from app.schemas import loan as schemas
from app.models import associate as associate_model
from app.models import book as book_model
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.Loan, status_code=status.HTTP_201_CREATED)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    # Check if the associate exists
    db_associate = db.query(associate_model.Associate).filter(associate_model.Associate.id == loan.associate_id).first()
    if not db_associate:
        raise HTTPException(status_code=404, detail="Associate not found")
    # Check if the book exists
    db_book = db.query(book_model.Book).filter(book_model.Book.id == loan.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Check if the book is currently available (not on loan)
    active_loans = crud.get_active_loans_for_book(db, book_id=loan.book_id)
    if active_loans:
        raise HTTPException(status_code=400, detail="Book is currently on loan")
    return crud.create_loan(db=db, loan=loan)

@router.get("/{loan_id}", response_model=schemas.Loan)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@router.get("/", response_model=list[schemas.Loan])
def read_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = crud.get_loans(db, skip=skip, limit=limit)
    return loans

@router.patch("/{loan_id}", response_model=schemas.Loan)
def update_loan(loan_id: int, loan: schemas.LoanUpdate, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return crud.update_loan(db=db, loan_id=loan_id, loan=loan)

@router.delete("/{loan_id}", response_model=schemas.Loan)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return crud.delete_loan(db=db, loan_id=loan_id)

# Return a book (set return_date to now)
@router.post("/{loan_id}/return", response_model=schemas.Loan)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    db_loan = crud.return_book(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    if db_loan.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    return db_loan

# Get active loans for a book
@router.get("/book/{book_id}/active-loans", response_model=list[schemas.Loan])
def read_active_loans_for_book(book_id: int, db: Session = Depends(get_db)):
    active_loans = crud.get_active_loans_for_book(db, book_id=book_id)
    return active_loans

# Get loans for an associate
@router.get("/associate/{associate_id}/loans", response_model=list[schemas.Loan])
def read_loans_for_associate(associate_id: int, db: Session = Depends(get_db)):
    loans = crud.get_loans_by_associate(db, associate_id=associate_id)
    return loans

# Get active loans for an associate
@router.get("/associate/{associate_id}/active-loans", response_model=list[schemas.Loan])
def read_active_loans_for_associate(associate_id: int, db: Session = Depends(get_db)):
    db_associate = db.query(associate_model.Associate).filter(associate_model.Associate.id == associate_id).first()
    if not db_associate:
        raise HTTPException(status_code=404, detail="Associate not found")
    active_loans = [loan for loan in db_associate.loans if loan.return_date is None]
    return active_loans