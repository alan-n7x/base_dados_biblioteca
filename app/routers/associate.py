from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import associate as crud
from app.schemas import associate as schemas
from app.models import library as library_model
from app.models import loan as loan_model

router = APIRouter()

@router.post("/", response_model=schemas.Associate, status_code=status.HTTP_201_CREATED)
def create_associate(associate: schemas.AssociateCreate, db: Session = Depends(get_db)):
    db_associate = crud.get_associate_by_registration(db, registration=associate.registration)
    if db_associate:
        raise HTTPException(status_code=400, detail="Associate with this registration already exists")
    return crud.create_associate(db=db, associate=associate)

@router.get("/{associate_id}", response_model=schemas.Associate)
def read_associate(associate_id: int, db: Session = Depends(get_db)):
    db_associate = crud.get_associate(db, associate_id=associate_id)
    if db_associate is None:
        raise HTTPException(status_code=404, detail="Associate not found")
    return db_associate

@router.get("/", response_model=list[schemas.Associate])
def read_associates(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    registration: Optional[str] = None,
    library_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    associates = crud.get_associates(
        db,
        skip=skip,
        limit=limit,
        name=name,
        registration=registration,
        library_id=library_id
    )
    return associates

@router.patch("/{associate_id}", response_model=schemas.Associate)
def update_associate(associate_id: int, associate: schemas.AssociateUpdate, db: Session = Depends(get_db)):
    db_associate = crud.get_associate(db, associate_id=associate_id)
    if db_associate is None:
        raise HTTPException(status_code=404, detail="Associate not found")
    return crud.update_associate(db=db, associate_id=associate_id, associate=associate)

@router.delete("/{associate_id}", response_model=schemas.Associate)
def delete_associate(associate_id: int, db: Session = Depends(get_db)):
    db_associate = crud.get_associate(db, associate_id=associate_id)
    if db_associate is None:
        raise HTTPException(status_code=404, detail="Associate not found")
    return crud.delete_associate(db=db, associate_id=associate_id)

# Get loans for an associate
@router.get("/{associate_id}/loans", response_model=list[schemas.Loan])
def read_associate_loans(associate_id: int, db: Session = Depends(get_db)):
    db_associate = crud.get_associate(db, associate_id=associate_id)
    if db_associate is None:
        raise HTTPException(status_code=404, detail="Associate not found")
    return db_associate.loans

# Get active loans for an associate (not returned yet)
@router.get("/{associate_id}/active-loans", response_model=list[schemas.Loan])
def read_associate_active_loans(associate_id: int, db: Session = Depends(get_db)):
    db_associate = crud.get_associate(db, associate_id=associate_id)
    if db_associate is None:
        raise HTTPException(status_code=404, detail="Associate not found")
    # Filter loans where return_date is None
    active_loans = [loan for loan in db_associate.loans if loan.return_date is None]
    return active_loans