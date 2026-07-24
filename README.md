# NLP & Digital Preservation Annotation Platform

An end-to-end platform for Assamese language annotation, translation, verification, and dataset export. Built for AI/ML dataset creation with community-driven quality control.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────┐
│  React + TS     │────▶│  FastAPI Backend  │────▶│ PostgreSQL │
│  (Vite + TW)    │     │  (Python 3.13)    │     │  (DB 15)   │
└─────────────────┘     └──────────────────┘     └────────────┘
         │                       │
         │                       ├── Firebase Storage (optional)
         │                       └── Local File Storage (default)
         │
    ┌────┴────┐
    │ Browser │
    └─────────┘
```

## Features

- **Role-Based Access**: Contributors (annotators), Verifiers, and Admins
- **Audio Upload**: Record voice via browser → upload to Firebase/local storage
- **QA Rule Engine**: Validates Assamese Unicode, filters toxic content
- **Syntax Tagging**: POS tagging, Named Entity Recognition for Assamese
- **Verification Flow**: Human review with +1/-1 voting, trust score tracking
- **Dataset Export**: CSV, JSON, and Parquet formats for AI/ML use
- **Admin Console**: User management, orphan cleanup, platform stats

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 22+
- PostgreSQL 15+ (or Docker)

### 1. Database Setup

```bash
# Option A: Using Docker (recommended)
docker compose up -d db

# Option B: Local PostgreSQL
psql -U postgres -c "CREATE DATABASE nlp_platform;"
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nlp_platform
SECRET_KEY=generate-a-random-64-char-hex-string
LOCAL_AUDIO_DIR=uploads/audio
```

Run migrations and seed data:

```bash
alembic upgrade head
python scripts/seed_phrases.py
```

Start the server:

```bash
uvicorn app.main:app --reload
```

API available at: http://127.0.0.1:8000  
Swagger docs: http://127.0.0.1:8000/docs

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: http://localhost:5173

### 4. Docker (Full Stack)

```bash
docker compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `SECRET_KEY` | Yes | `change-me-in-production` | JWT signing secret |
| `LOCAL_AUDIO_DIR` | No | `uploads/audio` | Local audio storage path |
| `FIREBASE_CREDENTIALS_PATH` | No | - | Firebase service account JSON path |
| `FIREBASE_STORAGE_BUCKET` | No | - | Firebase Storage bucket name |
| `VERIFICATION_APPROVAL_THRESHOLD` | No | `2` | Votes needed to verify |
| `VERIFICATION_REJECTION_THRESHOLD` | No | `2` | Votes needed to reject |
| `TRUST_SCORE_INCREMENT` | No | `1.0` | Score increase on approval |
| `TRUST_SCORE_PENALTY` | No | `2.0` | Score decrease on rejection |

## API Endpoints

### Authentication (`/auth`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Login |
| GET | `/auth/me` | Yes | Get current user |

### Audio (`/audio`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/audio/upload` | Yes | Upload audio file |

### Phrases (`/phrases`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/phrases` | No | List phrases (filter by status/language) |
| GET | `/phrases/random` | Yes | Get random unassigned phrase |
| GET | `/phrases/my` | Yes | List user's phrases |
| POST | `/phrases` | Yes | Submit raw phrase |
| GET | `/phrases/{id}` | No | Get phrase by ID |
| PUT | `/phrases/{id}` | Verifier | Update phrase |
| DELETE | `/phrases/{id}` | Admin | Delete phrase |

### Annotations (`/annotations`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/annotations` | No | List annotations |
| GET | `/annotations/my` | Yes | List user's annotations |
| POST | `/annotations` | Yes | Create annotation |
| GET | `/annotations/{id}` | No | Get annotation |
| PUT | `/annotations/{id}` | Owner/Admin | Update annotation |
| DELETE | `/annotations/{id}` | Owner/Admin | Delete annotation |

### Syntax Tagging (`/syntax`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/syntax/tag` | Yes | Tag text with POS/NE |

### Verifications (`/verifications`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/verifications` | Verifier | Cast vote |
| GET | `/verifications/pending` | Verifier | List pending annotations |
| GET | `/verifications/my` | Verifier | List user's votes |
| GET | `/verifications/{id}` | Verifier | Get votes for annotation |

### Export (`/export`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/export/csv` | Verifier | Download CSV |
| GET | `/export/json` | Verifier | Download JSON |
| GET | `/export/parquet` | Verifier | Download Parquet |
| GET | `/export/stats` | Verifier | Export statistics |

### Admin (`/admin`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/admin/users` | Admin | List all users |
| GET | `/admin/users/{id}` | Admin | Get user |
| PATCH | `/admin/users/{id}` | Admin | Update user |
| POST | `/admin/users/{id}/ban` | Admin | Ban user |
| POST | `/admin/users/{id}/unban` | Admin | Unban user |
| GET | `/admin/stats` | Admin | Platform statistics |
| GET | `/admin/dashboard` | Admin | Dashboard data |
| POST | `/admin/cleanup/orphans` | Admin | Cleanup orphaned audio |

## Roles

| Role | Permissions |
|------|-------------|
| **Admin** | All access: user management, cleanup, export, verification |
| **Verifier** | Review annotations, cast votes, export datasets |
| **Annotator** | Submit phrases, create annotations, record audio |

## Testing

### Backend
```bash
cd backend
pytest -v
```

### Frontend
```bash
cd frontend
npm test
npm run test:watch  # Watch mode
```

## Firebase Setup (Optional)

1. Go to https://console.firebase.google.com
2. Create project → Storage → Get Started (upgrade to Blaze plan)
3. Settings → Service Accounts → Generate New Private Key
4. Save JSON securely, reference in `.env`:
   ```
   FIREBASE_CREDENTIALS_PATH=C:/path/to/service-account.json
   FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   ```
5. Set Storage Rules:
   ```
   rules_version = '2';
   service firebase.storage {
     match /b/{bucket}/o {
       match /audio/{allPaths=**} {
         allow read: if true;
         allow write: if request.auth != null;
       }
     }
   }
   ```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── core/          # Config, security, dependencies
│   │   ├── db/            # Database connection
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routers/       # API routes
│   │   ├── services/      # Business logic
│   │   ├── qa/            # QA rule engine
│   │   └── main.py        # FastAPI app
│   ├── migrations/        # Alembic migrations
│   ├── scripts/           # Utility scripts
│   ├── tests/             # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── context/       # React context
│   │   ├── pages/         # Page components
│   │   ├── routes/        # Route config
│   │   ├── services/      # API client
│   │   ├── types/         # TypeScript types
│   │   └── __tests__/     # Frontend tests
│   └── package.json
├── docker-compose.yml
└── README.md
```
