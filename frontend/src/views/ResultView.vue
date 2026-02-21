<!--
  Result page: show score, per-question results with ChatGPT explanations.
-->
<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <LoadingSpinner v-if="store.loading" message="Đang tải kết quả..." />

    <template v-else-if="session">
      <!-- Score card -->
      <div class="bg-white border rounded-2xl p-6 text-center mb-8 shadow-sm">
        <p class="text-gray-500 text-sm mb-1">Chủ đề: {{ session.topic }}</p>
        <div class="text-6xl font-bold mb-2" :class="scoreColor">
          {{ session.score }}/{{ session.total }}
        </div>
        <p class="text-gray-600">{{ scoreLabel }}</p>
        <div class="flex justify-center gap-3 mt-4">
          <RouterLink
            to="/"
            class="px-5 py-2 rounded-lg border border-blue-600 text-blue-600 text-sm font-medium hover:bg-blue-50"
          >
            Thi lại
          </RouterLink>
          <RouterLink
            v-if="hasWrongAnswers"
            :to="{ name: 'review', params: { sessionId: session.id } }"
            class="px-5 py-2 rounded-lg bg-orange-500 text-white text-sm font-medium hover:bg-orange-600"
          >
            Ôn tập câu sai ({{ wrongCount }})
          </RouterLink>
          <RouterLink
            to="/history"
            class="px-5 py-2 rounded-lg border border-gray-300 text-gray-700 text-sm font-medium hover:bg-gray-50"
          >
            Lịch sử thi
          </RouterLink>
        </div>
      </div>

      <!-- All questions with results -->
      <div class="space-y-4">
        <QuestionCard
          v-for="q in session.questions"
          :key="q.id"
          :question="q"
          :interactive="false"
        />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useExamStore } from '@/stores/exam-store'
import QuestionCard from '@/components/QuestionCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import type { Question } from '@/types'

const props = defineProps<{ sessionId: number }>()
const store = useExamStore()

const session = computed(() => store.currentSession)
const wrongCount = computed(
  () => session.value?.questions.filter((q: Question) => !q.is_correct).length ?? 0,
)
const hasWrongAnswers = computed(() => wrongCount.value > 0)
const scorePercent = computed(() =>
  session.value ? (session.value.score ?? 0) / session.value.total : 0,
)
const scoreColor = computed(() => {
  if (scorePercent.value >= 0.8) return 'text-green-600'
  if (scorePercent.value >= 0.5) return 'text-yellow-600'
  return 'text-red-500'
})
const scoreLabel = computed(() => {
  if (scorePercent.value >= 0.8) return '🎉 Xuất sắc! Tiếp tục phát huy nhé.'
  if (scorePercent.value >= 0.5) return '👍 Khá tốt! Hãy ôn lại phần chưa đúng.'
  return '💪 Cần cố gắng thêm. Ôn tập và thử lại nhé!'
})

onMounted(async () => {
  if (!store.currentSession || store.currentSession.id !== props.sessionId) {
    await store.fetchSession(props.sessionId)
  }
})
</script>
