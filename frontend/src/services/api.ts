/**
 * Axios API client: all calls go to /api (proxied to FastAPI on port 8000)
 */
import axios, { type AxiosError } from 'axios'
import type { Topic, ExamSession, ExamHistoryItem, Question, PerformanceResponse, PerformanceInsight } from '@/types'

const http = axios.create({
  baseURL: '/api',
  timeout: 60000, // 60s to allow OpenAI calls to complete
  headers: { 'Content-Type': 'application/json' },
})

// Response interceptor: extract user-friendly error messages from API responses
http.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string | { msg: string }[] }>) => {
    if (!error.response) {
      // Network error or server down
      return Promise.reject(new Error('Không thể kết nối đến máy chủ. Vui lòng thử lại.'))
    }

    const detail = error.response.data?.detail
    let message: string

    if (Array.isArray(detail)) {
      // FastAPI validation error format: [{msg: "..."}]
      message = detail.map((d) => d.msg).join('; ')
    } else if (typeof detail === 'string') {
      message = detail
    } else {
      message = `Lỗi ${error.response.status}: Đã xảy ra lỗi không xác định.`
    }

    return Promise.reject(new Error(message))
  },
)

export const api = {
  // Topics
  getTopics(): Promise<Topic[]> {
    return http.get<Topic[]>('/topics').then((r) => r.data)
  },

  // Exams
  generateExam(topicId: number, numQuestions: number): Promise<ExamSession> {
    return http
      .post<ExamSession>('/exams/generate', { topic_id: topicId, num_questions: numQuestions })
      .then((r) => r.data)
  },

  submitExam(sessionId: number, answers: Record<number, string>): Promise<ExamSession> {
    return http
      .post<ExamSession>(`/exams/${sessionId}/submit`, { answers })
      .then((r) => r.data)
  },

  getHistory(): Promise<ExamHistoryItem[]> {
    return http.get<ExamHistoryItem[]>('/exams/history').then((r) => r.data)
  },

  getSession(sessionId: number): Promise<ExamSession> {
    return http.get<ExamSession>(`/exams/${sessionId}`).then((r) => r.data)
  },

  getReview(sessionId: number): Promise<Question[]> {
    return http.get<Question[]>(`/exams/${sessionId}/review`).then((r) => r.data)
  },

  // Analytics
  getPerformance(): Promise<PerformanceResponse> {
    return http.get<PerformanceResponse>('/analytics/performance').then((r) => r.data)
  },

  getInsights(): Promise<PerformanceInsight> {
    return http.get<PerformanceInsight>('/analytics/insights').then((r) => r.data)
  },
}
