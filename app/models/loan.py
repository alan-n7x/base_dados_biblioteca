from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
import datetime

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    associate_id = Column(Integer, ForeignKey("associates.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    loan_date = Column(DateTime, default=datetime.datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    # Relationships
    associate = relationship("Associate", back_populates="loans")
    book = relationship("Book", back_populates="loans")