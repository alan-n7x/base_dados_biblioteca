from sqlalchemy.orm import Session
from app.models import author as models
from app.schemas import author as schemas

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_author_by_code(db: Session, code: str):
    return db.query(models.Author).filter(models.Author.code == code).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100, name: Optional[str] = None, code: Optional[str] = None):
    query = db.query(models.Author)

    if name:
        query = query.filter(models.Author.name.ilike(f"%{name}%"))
    if code:
        query = query.filter(models.Author.code == code)

    return query.offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        code=author.code,
        name=author.name
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author:
        update_data = author.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_author, field, value)
        db.commit()
        db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author