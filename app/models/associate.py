from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

# Association table for associate and library (many-to-many)
associate_library = Table(
    "associate_library",
    Base.metadata,
    Column("associate_id", Integer, ForeignKey("associates.id")),
    Column("library_id", Integer, ForeignKey("libraries.id"))
)

class Associate(Base):
    __tablename__ = "associates"

    id = Column(Integer, primary_key=True, index=True)
    registration = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    sex = Column(String)
    # Removed library_id column; now using many-to-many relationship

    # Relationships
    libraries = relationship("Library", secondary=associate_library, back_populates="associates", cascade="all, delete")
    loans = relationship("Loan", back_populates="associate")

    @property
    def library_ids(self):
        return [lib.id for lib in self.libraries]