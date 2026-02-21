# Phase 1: Project Setup

## Context
- [plan.md](./plan.md)

## Overview
- **Priority:** P1
- **Status:** complete
- **Effort:** 2h
- Scaffold both frontend and backend projects, configure DB, set up dev tooling.

## Key Insights
- Use Poetry for Python dependency management (deterministic locks)
- Vite provides fast HMR for Vue 3 development
- docker-compose simplifies PostgreSQL setup
- Keep `.env.example` with all required env vars documented

## Requirements

### Functional
- Both frontend and backend projects runnable with single commands
- PostgreSQL accessible and migrations working
- Hot-reload for both frontend and backend in dev

### Non-Functional
- Dev environment reproducible via docker-compose
- Clear separation of frontend/backend concerns

## Related Code Files

### Files to Create
- `docker-compose.yml` - PostgreSQL service
- `.env.example` - Environment variable template
- `backend/pyproject.toml` - Python dependencies
- `backend/app/__init__.py`
- `backend/app/main.py` - FastAPI app entry
- `backend/app/core/__init__.py`
- `backend/app/core/config.py` - Settings via pydantic-settings
- `backend/app/core/database.py` - SQLAlchemy engine + session
- `backend/alembic.ini` - Alembic config
- `backend/alembic/env.py` - Alembic environment
- `frontend/package.json`
- `frontend/vite.config.ts`
- `frontend/tsconfig.json`
- `frontend/tailwind.config.js`
- `frontend/postcss.config.js`
- `frontend/src/main.ts` - App entry
- `frontend/src/App.vue`
- `frontend/index.html`

## Implementation Steps

### 1. Docker + Environment (15 min)

1. Create `docker-compose.yml` with PostgreSQL 15 service:
   ```yaml
   services:
     db:
       image: postgres:15
       environment:
         POSTGRES_USER: toeic
         POSTGRES_PASSWORD: toeic_dev
         POSTGRES_DB: toeic_exercise
       ports:
         - "5432:5432"
       volumes:
         - pgdata:/var/lib/postgresql/data
   volumes:
     pgdata:
   ```

2. Create `.env.example`:
   ```
   DATABASE_URL=postgresql://toeic:toeic_dev@localhost:5432/toeic_exercise
   OPENAI_API_KEY=sk-your-key-here
   OPENAI_MODEL=gpt-4o-mini
   CORS_ORIGINS=http://localhost:5173
   ```

### 2. Backend Setup (45 min)

1. Initialize Poetry project in `backend/`:
   ```bash
   cd backend && poetry init
   ```

2. Add dependencies to `pyproject.toml`:
   - `fastapi[standard]` - web framework
   - `uvicorn[standard]` - ASGI server
   - `sqlalchemy[asyncio]` - ORM
   - `asyncpg` - async PostgreSQL driver
   - `alembic` - migrations
   - `pydantic-settings` - config management
   - `openai` - OpenAI SDK
   - `python-dotenv` - env loading
   - Dev deps: `pytest`, `pytest-asyncio`, `httpx`

3. Create `backend/app/core/config.py`:
   - Use `pydantic_settings.BaseSettings` with `model_config` for `.env` loading
   - Fields: `DATABASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`, `CORS_ORIGINS`

4. Create `backend/app/core/database.py`:
   - `create_async_engine` with `DATABASE_URL`
   - `async_sessionmaker` for session factory
   - `get_db()` async generator dependency
   - `Base = declarative_base()`

5. Create `backend/app/main.py`:
   - FastAPI app with CORS middleware
   - Include API router (placeholder)
   - Health check endpoint `GET /api/health`

6. Initialize Alembic:
   ```bash
   cd backend && alembic init alembic
   ```
   - Update `alembic/env.py` to use async engine from config
   - Set `sqlalchemy.url` from `DATABASE_URL`

### 3. Frontend Setup (45 min)

1. Scaffold Vue 3 + TypeScript + Vite:
   ```bash
   npm create vite@latest frontend -- --template vue-ts
   ```

2. Install dependencies:
   ```bash
   npm install vue-router@4 pinia @pinia/plugin-persistedstate axios
   npm install -D tailwindcss @tailwindcss/vite
   ```

3. Configure Tailwind CSS:
   - Add Tailwind Vite plugin in `vite.config.ts`
   - Import `tailwindcss` in `src/style.css`

4. Configure Vite proxy for API:
   ```ts
   // vite.config.ts
   server: {
     proxy: {
       '/api': 'http://localhost:8000'
     }
   }
   ```

5. Set up Vue Router (`src/router/index.ts`):
   - Routes: `/` (topic selection), `/exam/:sessionId` (exam), `/history` (history), `/review/:sessionId` (review)

6. Set up Pinia store (`src/stores/index.ts`):
   - Register Pinia plugin in `main.ts`

7. Create API service (`src/services/api.ts`):
   - Axios instance with base URL `/api`
   - Type-safe API methods (stubs)

### 4. Verify Setup (15 min)

1. Start PostgreSQL: `docker-compose up -d`
2. Run backend: `cd backend && uvicorn app.main:app --reload`
3. Run frontend: `cd frontend && npm run dev`
4. Verify health endpoint: `curl http://localhost:8000/api/health`
5. Verify frontend loads at `http://localhost:5173`

## Todo List

- [ ] Create docker-compose.yml with PostgreSQL
- [ ] Create .env.example
- [ ] Initialize backend Poetry project with dependencies
- [ ] Create config.py with pydantic-settings
- [ ] Create database.py with async SQLAlchemy setup
- [ ] Create main.py with FastAPI app + CORS + health check
- [ ] Initialize Alembic for migrations
- [ ] Scaffold Vue 3 + TypeScript frontend with Vite
- [ ] Install and configure Tailwind CSS
- [ ] Configure Vite dev proxy to backend
- [ ] Set up Vue Router with route stubs
- [ ] Set up Pinia store
- [ ] Create API service layer with Axios
- [ ] Verify full dev stack runs end-to-end

## Success Criteria
- `docker-compose up -d` starts PostgreSQL
- Backend responds to `GET /api/health` with 200
- Frontend renders at `localhost:5173`
- Vite proxy forwards `/api/*` to backend
- Alembic can run migrations against PostgreSQL

## Risk Assessment
| Risk | Mitigation |
|------|------------|
| Port conflicts | Document expected ports, make configurable via .env |
| Poetry/npm version differences | Pin versions in README |

## Next Steps
- Proceed to [Phase 2: Backend Implementation](./phase-02-backend.md)
