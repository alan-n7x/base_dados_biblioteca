from typing import Optional
from sqlalchemy.orm import Session
from app.models import associate as models
from app.models import library as library_model
from app.schemas import associate as schemas

def get_associate(db: Session, associate_id: int):
    return db.query(models.Associate).filter(models.Associate.id == associate_id).first()

def get_associate_by_registration(db: Session, registration: str):
    return db.query(models.Associate).filter(models.Associate.registration == registration).first()

def get_associates(db: Session, skip: int = 0, limit: int = 100, name: Optional[str] = None, registration: Optional[str] = None, library_id: Optional[int] = None):
    query = db.query(models.Associate)

    if name:
        query = query.filter(models.Associate.name.ilike(f"%{name}%"))
    if registration:
        query = query.filter(models.Associate.registration.ilike(f"%{registration}%"))
    if library_id is not None:
        # Join via the association table to filter by library_id
        query = query.join(models.Associate.libraries).filter(library_model.Library.id == library_id)

    return query.offset(skip).limit(limit).all()

def create_associate(db: Session, associate: schemas.AssociateCreate):
    # Create associate instance without library_id
    db_associate = models.Associate(
        registration=associate.registration,
        name=associate.name,
        sex=associate.sex
    )
    # Associate with libraries if any provided
    if associate.library_ids:
        libraries = db.query(library_model.Library).filter(library_model.Library.id.in_(associate.library_ids)).all()
        db_associate.libraries.extend(libraries)
    db.add(db_associate)
    db.commit()
    db.refresh(db_associate)
    return db_associate

def update_associate(db: Session, associate_id: int, associate: schemas.AssociateUpdate):
    db_associate = db.query(models.Associate).filter(models.Associate.id == associate_id).first()
    if db_associate:
        update_data = associate.dict(exclude_unset=True)
        # Handle library_ids separately
        if 'library_ids' in update_data:
            library_ids = update_data.pop('library_ids')
            # Update the associated libraries
            if library_ids is not None:
                libraries = db.query(library_model.Library).filter(library_model.Library.id.in_(library_ids)).all()
                db_associate.libraries = libraries
            else:
                # If explicitly set to None, clear associations? We'll keep as empty list.
                db_associate.libraries = []
        # Update other fields
        for field, value in update_data.items():
            setattr(db_associate, field, value)
        db.commit()
        db.refresh(db_associate)
    return db_associate

def delete_associate(db: Session, associate_id: int):
    db_associate = db.query(models.Associate).filter(models.Associate.id == associate_id).first()
    if db_associate:
        db.delete(db_associate)
        db.commit()
    return db_associate