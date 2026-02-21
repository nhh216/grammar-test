export interface Topic {
  id: number
  name: string
  slug: string
  description: string
  summary?: string | null
}

export interface Question {
  id: number
  question_number: number
  question_text: string
  options: Record<string, string>
  correct_answer: string | null
  user_answer: string | null
  is_correct: boolean | null
  explanation: string | null
}

export interface ExamSession {
  id: number
  topic: string
  num_questions: number
  score: number | null
  total: number
  status: 'in_progress' | 'completed'
  created_at: string
  completed_at: string | null
  questions: Question[]
}

export interface TopicPerformance {
  topic_id: number
  topic_name: string
  slug: string
  sessions_completed: number
  total_questions: number
  total_correct: number
  accuracy_pct: number
  avg_score_pct: number
  level: 'weak' | 'moderate' | 'strong' | 'untested'
  trend: 'improving' | 'declining' | 'stable' | 'new'
  recent_scores: number[]
}

export interface PerformanceResponse {
  topics: TopicPerformance[]
  total_sessions: number
  total_questions_answered: number
  overall_accuracy: number
  has_data: boolean
}

export interface PerformanceInsight {
  overall_level: string
  overall_accuracy: number
  summary: string
  weak_topics: string[]
  strong_topics: string[]
  recommendations: string[]
  study_plan: string
}

export interface ExamHistoryItem {
  id: number
  topic: string
  score: number | null
  total: number
  status: 'in_progress' | 'completed'
  created_at: string
}
