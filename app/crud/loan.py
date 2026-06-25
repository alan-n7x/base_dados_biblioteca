from sqlalchemy.orm import Session
from app.models import loan as models
from app.schemas import loan as schemas
from datetime import datetime

def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loans_by_associate(db: Session, associate_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Loan).filter(models.Loan.associate_id == associate_id).offset(skip).limit(limit).all()

def get_loans_by_book(db: Session, book_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Loan).filter(models.Loan.book_id == book_id).offset(skip).limit(limit).all()

def get_active_loans_for_book(db: Session, book_id: int):
    # Returns loans that are not yet returned (return_date is None)
    return db.query(models.Loan).filter(models.Loan.book_id == book_id, models.Loan.return_date == None).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = models.Loan(
        associate_id=loan.associate_id,
        book_id=loan.book_id,
        loan_date=loan.loan_date or datetime.utcnow(),
        return_date=loan.return_date
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def update_loan(db: Session, loan_id: int, loan: schemas.LoanUpdate):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if db_loan:
        update_data = loan.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_loan, field, value)
        db.commit()
        db.refresh(db_loan)
    return db_loan

def delete_loan(db: Session, loan_id: int):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if db_loan:
        db.delete(db_loan)
        db.commit()
    return db_loan

def return_book(db: Session, loan_id: int):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if db_loan and db_loan.return_date is None:
        db_loan.return_date = datetime.utcnow()
        db.commit()
        db.refresh(db_loan)
    return db_loan