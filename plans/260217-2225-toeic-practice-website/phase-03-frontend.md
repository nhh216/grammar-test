# Phase 3: Frontend Implementation

## Context
- [plan.md](./plan.md)
- Depends on: [Phase 2](./phase-02-backend.md) completed (API endpoints available)

## Overview
- **Priority:** P1
- **Status:** complete
- **Effort:** 6h
- Build Vue 3 SPA with topic selection, exam taking, grading results, history, and review mode.

## Key Insights
- Keep component count minimal for MVP; avoid premature abstraction
- Use Pinia for exam state (questions, answers, results) to survive page navigation
- Tailwind utility classes for rapid UI - no custom CSS needed
- Axios interceptors handle loading/error states globally

## Requirements

### Functional
- Topic selection page with grid of grammar topics
- Exam page: display questions one-at-a-time or all-at-once, collect answers, submit
- Results page: show score, per-question grading with explanations
- History page: list past exams with scores
- Review page: re-practice wrong questions from a past exam

### Non-Functional
- Mobile-responsive (Tailwind breakpoints)
- Loading indicators during OpenAI API calls
- Error handling with user-friendly messages

## Architecture

```
Views (pages):
  HomeView.vue        -> Topic selection grid
  ExamView.vue        -> Take exam (questions + submit)
  ResultView.vue      -> Graded results with explanations
  HistoryView.vue     -> Past exam sessions list
  ReviewView.vue      -> Re-practice wrong answers

Stores:
  exam-store.ts       -> Current exam state (session, questions, answers)

Services:
  api.ts              -> Typed Axios wrapper for all endpoints

Components:
  QuestionCard.vue    -> Single question with options (reused in exam + review)
  TopicCard.vue       -> Topic selection card
  ExamSummary.vue     -> Score display + stats
  LoadingSpinner.vue  -> Loading state
  NavBar.vue          -> Top navigation
```

## Related Code Files

### Files to Create
- `frontend/src/types/index.ts` - TypeScript interfaces
- `frontend/src/services/api.ts` - API client
- `frontend/src/stores/exam-store.ts` - Pinia exam store
- `frontend/src/router/index.ts` - Vue Router config
- `frontend/src/components/nav-bar.vue`
- `frontend/src/components/topic-card.vue`
- `frontend/src/components/question-card.vue`
- `frontend/src/components/exam-summary.vue`
- `frontend/src/components/loading-spinner.vue`
- `frontend/src/views/home-view.vue`
- `frontend/src/views/exam-view.vue`
- `frontend/src/views/result-view.vue`
- `frontend/src/views/history-view.vue`
- `frontend/src/views/review-view.vue`

### Files to Modify
- `frontend/src/App.vue` - Add NavBar + router-view
- `frontend/src/main.ts` - Register Pinia + Router
- `frontend/src/style.css` - Tailwind imports

## Implementation Steps

### 1. TypeScript Interfaces (15 min)

#### `frontend/src/types/index.ts`
```typescript
export interface Topic {
  id: number
  name: string
  slug: string
  description: string
}

export interface Question {
  id: number
  question_number: number
  question_text: string
  options: Record<string, string>  // {A: "...", B: "...", C: "...", D: "..."}
  correct_answer?: string
  user_answer?: string
  is_correct?: boolean
  explanation?: string
}

export interface ExamSession {
  id: number
  topic: string
  num_questions: number
  score: number | null
  total: number
  status: string
  created_at: string
  completed_at: string | null
  questions: Question[]
}

export interface ExamHistoryItem {
  id: number
  topic: string
  score: number | null
  total: number
  status: string
  created_at: string
}
```

### 2. API Service (30 min)

#### `frontend/src/services/api.ts`
```typescript
import axios from 'axios'
import type { Topic, ExamSession, ExamHistoryItem, Question } from '@/types'

const client = axios.create({ baseURL: '/api' })

export const api = {
  getTopics: () =>
    client.get<Topic[]>('/topics').then(r => r.data),

  generateExam: (topicId: number, numQuestions: number) =>
    client.post<ExamSession>('/exams/generate', {
      topic_id: topicId,
      num_questions: numQuestions
    }).then(r => r.data),

  submitExam: (sessionId: number, answers: Record<number, string>) =>
    client.post<ExamSession>(`/exams/${sessionId}/submit`, { answers }).then(r => r.data),

  getHistory: (limit = 20, offset = 0) =>
    client.get<ExamHistoryItem[]>('/exams/history', { params: { limit, offset } }).then(r => r.data),

  getExam: (sessionId: number) =>
    client.get<ExamSession>(`/exams/${sessionId}`).then(r => r.data),

  getReview: (sessionId: number) =>
    client.get<Question[]>(`/exams/${sessionId}/review`).then(r => r.data),
}
```

### 3. Pinia Store (30 min)

#### `frontend/src/stores/exam-store.ts`
```typescript
export const useExamStore = defineStore('exam', {
  state: () => ({
    currentSession: null as ExamSession | null,
    answers: {} as Record<number, string>,  // questionId -> selected option
    isLoading: false,
    error: null as string | null,
  }),

  getters: {
    answeredCount: (state) => Object.keys(state.answers).length,
    allAnswered: (state) =>
      state.currentSession
        ? Object.keys(state.answers).length === state.currentSession.num_questions
        : false,
  },

  actions: {
    async generateExam(topicId: number, numQuestions: number) { ... },
    setAnswer(questionId: number, answer: string) { ... },
    async submitExam() { ... },
    reset() { ... },
  },
})
```

### 4. Reusable Components (1h)

#### `frontend/src/components/nav-bar.vue`
- App title "TOEIC Grammar Practice"
- Nav links: Home, History
- Tailwind: sticky top, shadow, white bg

#### `frontend/src/components/topic-card.vue`
- Props: `topic: Topic`
- Emit: `select`
- Display: topic name, description, "Start" button
- Tailwind: card with border, hover shadow, rounded

#### `frontend/src/components/question-card.vue`
- Props: `question: Question`, `selectedAnswer: string | null`, `showResult: boolean`
- Emit: `select(answer: string)`
- Display: question text, 4 radio options (A-D)
- When `showResult=true`: highlight correct (green), incorrect (red), show explanation
- This component is reused in ExamView, ResultView, and ReviewView

#### `frontend/src/components/exam-summary.vue`
- Props: `session: ExamSession`
- Display: topic, score/total, percentage, date

#### `frontend/src/components/loading-spinner.vue`
- Simple centered spinner with "Generating questions..." or custom message
- Props: `message: string`

### 5. View Pages (3h)

#### `frontend/src/views/home-view.vue` (30 min)
- Fetch topics on mount via `api.getTopics()`
- Display as responsive grid of TopicCard components
- On topic select: show number-of-questions selector (dropdown: 5, 10, 15, 20)
- "Start Exam" button calls `examStore.generateExam()` then navigates to `/exam/:id`
- Show LoadingSpinner during generation

#### `frontend/src/views/exam-view.vue` (45 min)
- Get session from exam store (redirect to home if empty)
- Display all questions using QuestionCard (scroll layout)
- Track answers in store via `examStore.setAnswer()`
- Progress indicator: "X of Y answered"
- "Submit Exam" button (disabled until all answered)
- Confirmation dialog before submit
- On submit: call `examStore.submitExam()`, navigate to `/result/:id`
- Show LoadingSpinner during grading

#### `frontend/src/views/result-view.vue` (30 min)
- Fetch session via `api.getExam(sessionId)` or use store
- ExamSummary at top (score, percentage)
- List all questions with QuestionCard in `showResult=true` mode
- Show correct/incorrect status and explanations
- Buttons: "Back to Home", "View History"

#### `frontend/src/views/history-view.vue` (30 min)
- Fetch history via `api.getHistory()`
- Table/list: topic, score, date, status
- Click row -> navigate to result view for that session
- Empty state if no history
- Simple pagination (load more button)

#### `frontend/src/views/review-view.vue` (30 min)
- Fetch wrong questions via `api.getReview(sessionId)`
- Display each wrong question with QuestionCard
- User can re-select answers (practice mode, no submission)
- Show/hide correct answer toggle
- Link back to full result view

### 6. Router Configuration (15 min)

```typescript
const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/exam/:sessionId', name: 'exam', component: ExamView },
  { path: '/result/:sessionId', name: 'result', component: ResultView },
  { path: '/history', name: 'history', component: HistoryView },
  { path: '/review/:sessionId', name: 'review', component: ReviewView },
]
```

### 7. App Shell (15 min)

Update `App.vue`:
```vue
<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />
    <main class="container mx-auto px-4 py-8 max-w-4xl">
      <router-view />
    </main>
  </div>
</template>
```

## Todo List

- [ ] Define TypeScript interfaces for all data types
- [ ] Implement API service with typed Axios methods
- [ ] Create Pinia exam store with generate/submit actions
- [ ] Build NavBar component
- [ ] Build TopicCard component
- [ ] Build QuestionCard component (supports exam + review modes)
- [ ] Build ExamSummary component
- [ ] Build LoadingSpinner component
- [ ] Implement HomeView (topic selection + exam config)
- [ ] Implement ExamView (answer questions + submit)
- [ ] Implement ResultView (graded results + explanations)
- [ ] Implement HistoryView (past exams list)
- [ ] Implement ReviewView (re-practice wrong answers)
- [ ] Configure Vue Router with all routes
- [ ] Update App.vue shell with NavBar + router-view

## Success Criteria
- User can select topic and question count, then start exam
- Questions display correctly with selectable options
- Submit grays out until all questions answered
- Results show score and per-question explanations with color coding
- History lists all past exams
- Review mode shows only wrong questions with explanations
- Mobile-responsive layout

## Risk Assessment
| Risk | Mitigation |
|------|------------|
| Long loading during question generation | LoadingSpinner with message, disable navigation |
| User navigates away mid-exam | Pinia state persists; add beforeRouteLeave guard |
| Large question text overflow | Tailwind `break-words`, test with long text |

## Next Steps
- Proceed to [Phase 4: Integration & Testing](./phase-04-integration.md)
