# Biblioteca API

A FastAPI application for managing a library system.

## Features

- Manage libraries, associates, books, authors, subjects, and loans
- Associates can be registered in multiple libraries (many‑to‑many relationship)
- RESTful API with automatic documentation (Swagger UI)
- SQLAlchemy ORM with SQLite database
- Pydantic models for data validation

## Requirements

- Python 3.8+
- Dependencies in `requirements.txt`

## Installation

1. Clone the repository
2. Create a virtual environment (optional but recommended)
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser to `http://localhost:8000/docs` for the interactive API documentation.

3. Alternatively, use `http://localhost:8000/redoc` for ReDoc documentation.

## API Endpoints

- Libraries: `/libraries`
- Associates: `/associates`
- Books: `/books`
- Authors: `/authors`
- Subjects: `/subjects`
- Loans: `/loans`

### Associates

Associates now support a list of library IDs via the `library_ids` field.

**Create an associate**

```json
POST /associates
{
  "registration": "12345",
  "name": "João Silva",
  "sex": "M",
  "library_ids": [1, 3, 5]
}
```

**Update an associate**

```json
PATCH /associates/{id}
{
  "library_ids": [2, 4]
}
```

**Filter associates by library**

```
GET /associates?library_id=2
```

## Database

The application uses SQLite by default. The database file is `biblioteca.db` in the project root.

To use a different database, modify the `SQLALCHEMY_DATABASE_URL` in `app/db/session.py`.

## License

This project is licensed under the MIT License.