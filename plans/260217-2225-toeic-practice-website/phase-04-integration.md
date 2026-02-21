# Phase 4: Integration & Testing

## Context
- [plan.md](./plan.md)
- Depends on: [Phase 2](./phase-02-backend.md) + [Phase 3](./phase-03-frontend.md) completed

## Overview
- **Priority:** P1
- **Status:** complete
- **Effort:** 2h
- End-to-end integration testing, error handling polish, and deployment prep.

## Key Insights
- Focus on happy-path E2E testing for MVP
- Backend pytest with httpx AsyncClient for API tests
- Frontend relies on manual testing for MVP (add Vitest unit tests for stores)
- Docker Compose can orchestrate full stack for demo

## Requirements

### Functional
- Full user flow works end-to-end: select topic -> take exam -> view results -> review
- Error states handled gracefully (API down, OpenAI failure, network issues)

### Non-Functional
- Backend API tests cover all endpoints
- Frontend builds without errors
- Docker Compose runs full stack

## Implementation Steps

### 1. Backend API Tests (45 min)

#### `backend/tests/conftest.py`
- Create async test fixtures: test DB session, test client
- Use SQLite in-memory or test PostgreSQL database
- Mock OpenAI service for deterministic tests

#### `backend/tests/test-topics.py`
- Test GET /api/topics returns seeded topics
- Test response schema matches TopicResponse

#### `backend/tests/test-exams.py`
- Test POST /api/exams/generate with mocked OpenAI
- Test POST /api/exams/{id}/submit with mocked grading
- Test GET /api/exams/history returns sessions
- Test GET /api/exams/{id} returns session detail
- Test GET /api/exams/{id}/review returns only wrong answers
- Test validation errors (invalid topic_id, out-of-range num_questions)

### 2. Frontend Store Tests (30 min)

#### `frontend/src/stores/__tests__/exam-store.test.ts`
- Test generateExam action calls API and sets state
- Test setAnswer updates answers map
- Test submitExam sends correct payload
- Test reset clears state
- Mock API service

### 3. Error Handling Polish (20 min)

#### Backend
- Global exception handler in FastAPI for unhandled errors
- Specific error responses:
  - 404: Session not found
  - 400: Invalid answers (missing questions, invalid option)
  - 502: OpenAI API failure (with user-friendly message)
  - 422: Validation errors (auto-handled by FastAPI)

#### Frontend
- Axios response interceptor for error toast/alert
- ExamView: handle generation failure (show error, allow retry)
- SubmitView: handle grading failure (show error, allow retry)
- Network error fallback message

### 4. Docker Compose Full Stack (15 min)

Update `docker-compose.yml`:
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

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://toeic:toeic_dev@db:5432/toeic_exercise
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

volumes:
  pgdata:
```

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev
COPY . .
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

Create `frontend/nginx.conf`:
- Serve SPA with fallback to `index.html`
- Proxy `/api` to backend service

### 5. End-to-End Manual Test Checklist (10 min)

Run through complete flow:
1. Start stack: `docker-compose up -d`
2. Open `http://localhost:5173`
3. Verify topics load on home page
4. Select a topic, choose 5 questions
5. Verify loading spinner during generation
6. Answer all questions, submit
7. Verify loading during grading
8. Check results page shows score + explanations
9. Navigate to history, verify session listed
10. Click review, verify wrong questions shown
11. Test error case: stop backend, verify frontend error message

## Todo List

- [x] Create backend test fixtures (conftest.py)
- [x] Write API tests for topics endpoint
- [x] Write API tests for exam endpoints (with mocked OpenAI)
- [x] Write Pinia store unit tests
- [x] Add global error handler to FastAPI
- [x] Add Axios error interceptor to frontend
- [x] Create backend Dockerfile
- [x] Create frontend Dockerfile + nginx.conf
- [x] Update docker-compose.yml for full stack
- [x] Run E2E manual test checklist
- [x] Create README.md with setup instructions

## Success Criteria
- `pytest` passes all backend tests
- `npm run build` succeeds without errors
- `docker-compose up` runs full stack
- Complete user flow works end-to-end
- Error states show user-friendly messages

## Risk Assessment
| Risk | Mitigation |
|------|------------|
| Flaky tests from async timing | Use proper async test fixtures, avoid sleep |
| Docker build slow | Multi-stage builds, layer caching |
| CORS issues in production | Nginx proxies /api, no CORS needed |

## Security Considerations
- OPENAI_API_KEY only in backend env, never exposed to frontend
- .env file in .gitignore
- Nginx does not expose backend directly

## Unresolved Questions
- Do we need user authentication for MVP? (Assumed no - single user)
- Should we add rate limiting on exam generation? (Deferred to v2)
- Do we want to support exam timer? (Not in MVP scope)
