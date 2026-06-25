from sqlalchemy.orm import Session
from app.models import subject as models
from app.schemas import subject as schemas
from typing import Optional

def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()

def get_subject_by_code(db: Session, code: str):
    return db.query(models.Subject).filter(models.Subject.code == code).first()

def get_subjects(db: Session, skip: int = 0, limit: int = 100, description: Optional[str] = None, code: Optional[str] = None):
    query = db.query(models.Subject)

    if description:
        query = query.filter(models.Subject.description.ilike(f"%{description}%"))
    if code:
        query = query.filter(models.Subject.code == code)

    return query.offset(skip).limit(limit).all()

def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(
        code=subject.code,
        description=subject.description
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def update_subject(db: Session, subject_id: int, subject: schemas.SubjectUpdate):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if db_subject:
        update_data = subject.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_subject, field, value)
        db.commit()
        db.refresh(db_subject)
    return db_subject

def delete_subject(db: Session, subject_id: int):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if db_subject:
        db.delete(db_subject)
        db.commit()
    return db_subject