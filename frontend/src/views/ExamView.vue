<!--
  Exam page: answer all questions, then submit for AI grading.
-->
<template>
  <div class="max-w-3xl mx-auto px-4 py-6 sm:py-8 pb-24 sm:pb-8">
    <LoadingSpinner v-if="store.loading" :message="loadingMessage" />

    <template v-else-if="session">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900">{{ session.topic }}</h1>
        <p class="text-sm text-gray-500 mt-1">
          {{ answeredCount }} / {{ session.questions.length }} câu đã trả lời
        </p>
        <!-- Progress bar -->
        <div class="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="h-full bg-blue-500 transition-all duration-300"
            :style="{ width: `${(answeredCount / session.questions.length) * 100}%` }"
          />
        </div>
      </div>

      <!-- Questions -->
      <div class="space-y-4 mb-8">
        <QuestionCard
          v-for="q in session.questions"
          :key="q.id"
          :question="q"
          :selectedAnswer="store.userAnswers[q.id]"
          :interactive="true"
          @answer="store.setAnswer"
        />
      </div>

      <!-- Submit -->
      <div class="fixed bottom-0 left-0 right-0 sm:static sm:bottom-auto z-10 bg-white/90 sm:bg-transparent backdrop-blur-sm sm:backdrop-blur-none border-t sm:border-0 border-gray-200 px-4 py-3 sm:p-0">
        <div class="max-w-3xl mx-auto">
          <button
            class="w-full bg-green-600 text-white py-3 sm:py-3 rounded-xl font-semibold text-base sm:text-lg hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-lg"
            :disabled="answeredCount < session.questions.length"
            @click="submit"
          >
            Nộp bài ({{ answeredCount }}/{{ session.questions.length }} câu)
          </button>
        </div>
      </div>
    </template>

    <div v-else class="text-center text-gray-500 py-16">
      Không tìm thấy bài thi. <RouterLink to="/" class="text-blue-600 underline">Về trang chủ</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExamStore } from '@/stores/exam-store'
import QuestionCard from '@/components/QuestionCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import type { Question } from '@/types'

const props = defineProps<{ sessionId: number }>()
const store = useExamStore()
const router = useRouter()
const loadingMessage = ref('Đang tải...')

const session = computed(() => store.currentSession)

const answeredCount = computed(() =>
  session.value?.questions.filter((q: Question) => store.userAnswers[q.id]).length ?? 0,
)

onMounted(async () => {
  // If store already has this session, use it; otherwise fetch
  if (!store.currentSession || store.currentSession.id !== props.sessionId) {
    await store.fetchSession(props.sessionId)
  }
})

async function submit() {
  loadingMessage.value = 'ChatGPT đang chấm bài và giải thích đáp án...'
  const ok = await store.submitExam(props.sessionId)
  if (ok) router.push({ name: 'result', params: { sessionId: props.sessionId } })
}
</script>
