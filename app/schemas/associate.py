from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AssociateBase(BaseModel):
    name: str
    sex: str  # Assuming values like 'M', 'F', or other
    registration: str  # matrícula
    library_ids: List[int] = []

    class Config:
        from_attributes = True

class AssociateCreate(AssociateBase):
    pass

class AssociateUpdate(AssociateBase):
    name: Optional[str] = None
    sex: Optional[str] = None
    registration: Optional[str] = None
    # library_ids inherited from AssociateBase

class AssociateInDBBase(AssociateBase):
    id: int

    class Config:
        from_attributes = True

class Associate(AssociateInDBBase):
    pass

class AssociateWithLoans(AssociateInDBBase):
    loans: list = []

    class Config:
        from_attributes = True

# Avoid circular import by using forward references
from .loan import Loan, LoanInDBBase

AssociateWithLoans.model_rebuild()