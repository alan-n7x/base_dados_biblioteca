from fastapi import FastAPI
from app.routers import library, associate, book, author, loan
from app.db.session import Base, engine

app = FastAPI(
    title="Biblioteca API",
    description="API for managing a library system",
    version="0.1.0",
)

# Create tables
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(library.router, prefix="/libraries", tags=["libraries"])
app.include_router(associate.router, prefix="/associates", tags=["associates"])
app.include_router(book.router, prefix="/books", tags=["books"])
app.include_router(author.router, prefix="/authors", tags=["authors"])
app.include_router(loan.router, prefix="/loans", tags=["loans"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Biblioteca API"}