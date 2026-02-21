/**
 * Pinia store for exam state management.
 * Persists current session to localStorage so page refresh doesn't lose exam progress.
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/services/api'
import type { ExamSession, Topic, ExamHistoryItem, Question } from '@/types'

export const useExamStore = defineStore(
  'exam',
  () => {
    // State
    const topics = ref<Topic[]>([])
    const currentSession = ref<ExamSession | null>(null)
    const userAnswers = ref<Record<number, string>>({})
    const history = ref<ExamHistoryItem[]>([])
    const reviewQuestions = ref<Question[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    // Actions
    async function fetchTopics() {
      loading.value = true
      error.value = null
      try {
        topics.value = await api.getTopics()
      } catch (e: unknown) {
        error.value = getErrorMessage(e)
      } finally {
        loading.value = false
      }
    }

    async function startExam(topicId: number, numQuestions: number): Promise<number | null> {
      loading.value = true
      error.value = null
      userAnswers.value = {}
      try {
        const session = await api.generateExam(topicId, numQuestions)
        currentSession.value = session
        return session.id
      } catch (e: unknown) {
        error.value = getErrorMessage(e)
        return null
      } finally {
        loading.value = false
      }
    }

    function setAnswer(questionId: number, answer: string) {
      userAnswers.value[questionId] = answer
    }

    async function submitExam(sessionId: number): Promise<boolean> {
      loading.value = true
      error.value = null
      try {
        const result = await api.submitExam(sessionId, userAnswers.value)
        currentSession.value = result
        return true
      } catch (e: unknown) {
        error.value = getErrorMessage(e)
        return false
      } finally {
        loading.value = false
      }
    }

    async function fetchHistory() {
      loading.value = true
      error.value = null
      try {
        history.value = await api.getHistory()
      } catch (e: unknown) {
        error.value = getErrorMessage(e)
      } finally {
        loading.value = false
      }
    }

    async function fetchSession(sessionId: number) {
      loading.value = true
      error.value = null
      try {
        currentSession.value = await api.getSession(sessionId)
      } catch (e: unknown) {
        error.value = getErrorMessage(e)
      } finally {
        loading.value = false
      }
    }

    async function fetchReview(sessionId: number) {
      loading.value = true
      error.value = null
      try {
        reviewQuestions.value = await api.getReview(sessionId)
      } catch (e: unknown) {
        error.value = getErrorMessage(e)
      } finally {
        loading.value = false
      }
    }

    function clearError() {
      error.value = null
    }

    return {
      topics,
      currentSession,
      userAnswers,
      history,
      reviewQuestions,
      loading,
      error,
      fetchTopics,
      startExam,
      setAnswer,
      submitExam,
      fetchHistory,
      fetchSession,
      fetchReview,
      clearError,
    }
  },
  { persist: { pick: ['currentSession', 'userAnswers'] } },
)

function getErrorMessage(e: unknown): string {
  if (e instanceof Error) return e.message
  return 'An unexpected error occurred'
}
