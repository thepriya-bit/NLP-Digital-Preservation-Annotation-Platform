# Assamese NLP Platform Backend

This project provides a FastAPI backend for an Assamese NLP platform with PostgreSQL, SQLAlchemy 2.x, and Alembic migrations.

## 1. Software Installation

Install the following:
- Python 3.12+
- PostgreSQL 15+
- VS Code
- Git

## 2. Python Installation

On Windows:
1. Download Python from https://www.python.org/downloads/
2. Install it and ensure "Add Python to PATH" is checked.
3. Verify:
   ```bash
   python --version
   pip --version
   ```

## 3. PostgreSQL Installation

Install PostgreSQL and start the server.

## 4. VS Code Setup

Install these extensions:
- Python
- Pylance
- PostgreSQL

## 5. Virtual Environment

From the project root:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
```

## 6. Install Requirements

```bash
pip install -r requirements.txt
```

## 7. Configure PostgreSQL

Create a database named `nlp_platform`.

```sql
CREATE DATABASE nlp_platform;
```

## 8. Configure .env

Copy the example file and update the connection string:
```bash
copy .env.example .env
```

Example:
```env
APP_NAME=NLP Platform
DATABASE_URL=postgresql://postgres:password@localhost:5432/nlp_platform
```

## 9. Run Alembic

```bash
alembic revision --autogenerate -m "Initial Migration"
alembic upgrade head
```

## 10. Run FastAPI

```bash
uvicorn app.main:app --reload
```

## 11. Verify Database

You can verify tables with:
```sql
\dt
```

## 12. Verify JSONB

```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name='annotations';
```

## 13. Verify GIN Index

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename='annotations';
```

## 14. Test API

Open the following URLs:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
