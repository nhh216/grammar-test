---
title: "TOEIC Grammar Practice Website"
description: "Full-stack TOEIC grammar practice app with AI-powered question generation and grading"
status: completed
priority: P1
effort: 16h
branch: main
tags: [vue3, fastapi, openai, postgresql, toeic]
created: 2026-02-17
completed: 2026-02-18
---

# TOEIC Grammar Practice Website - Implementation Plan

## Overview

Build an MVP TOEIC grammar practice website where users select grammar topics, take AI-generated multiple-choice exams, receive graded explanations, and review past mistakes.

**Tech Stack:** Vue 3 + TypeScript + Vite + Tailwind (frontend) | FastAPI + SQLAlchemy + Alembic (backend) | PostgreSQL | OpenAI GPT-4o-mini

## Architecture

```
toeic-exercise/
├── frontend/             # Vue 3 + Vite
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── views/        # Page-level components
│   │   ├── stores/       # Pinia state management
│   │   ├── router/       # Vue Router config
│   │   ├── services/     # API client layer
│   │   └── types/        # TypeScript interfaces
│   └── package.json
├── backend/              # FastAPI
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Business logic + OpenAI integration
│   │   └── core/         # Config, DB session, dependencies
│   ├── alembic/          # Database migrations
│   └── pyproject.toml
├── docker-compose.yml    # PostgreSQL + app services
└── .env.example
```

## Phases

| # | Phase | Status | Effort | Details |
|---|-------|--------|--------|---------|
| 1 | Project Setup | complete | 2h | [phase-01-setup.md](./phase-01-setup.md) |
| 2 | Backend Implementation | complete | 6h | [phase-02-backend.md](./phase-02-backend.md) |
| 3 | Frontend Implementation | complete | 6h | [phase-03-frontend.md](./phase-03-frontend.md) |
| 4 | Integration & Testing | complete | 2h | [phase-04-integration.md](./phase-04-integration.md) |

## Key Dependencies

- OpenAI API key (GPT-4o-mini)
- PostgreSQL 15+
- Node.js 18+ / Python 3.11+
- Docker (optional, for DB)

## Database Schema (Summary)

- `grammar_topics` - predefined TOEIC grammar topics
- `exam_sessions` - each exam attempt with topic, score, timestamps
- `questions` - individual questions with options, answers, explanations

## API Endpoints (Summary)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/topics` | List grammar topics |
| POST | `/api/exams/generate` | Generate exam via GPT |
| POST | `/api/exams/submit` | Submit + grade via GPT |
| GET | `/api/exams/history` | Past exam sessions |
| GET | `/api/exams/{id}` | Exam detail |
| GET | `/api/exams/{id}/review` | Wrong answers for review |

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| OpenAI API latency (5-15s for generation) | Show loading state, stream if possible |
| GPT output format inconsistency | Strict JSON schema in prompt + Pydantic validation |
| Cost per exam (~$0.01-0.02 with gpt-4o-mini) | Rate limiting, session-based caching |
| No auth in MVP | Accept for MVP, plan auth in v2 |
