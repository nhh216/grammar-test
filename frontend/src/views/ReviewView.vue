<!--
  Review page: show only incorrectly answered questions from a past exam.
-->
<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="mb-6 flex items-center gap-4">
      <RouterLink to="/history" class="text-blue-600 hover:underline text-sm">← Lịch sử</RouterLink>
      <h1 class="text-2xl font-bold text-gray-900">Ôn tập câu sai</h1>
    </div>

    <LoadingSpinner v-if="store.loading" message="Đang tải câu hỏi ôn tập..." />

    <template v-else>
      <div v-if="store.reviewQuestions.length === 0" class="text-center text-gray-400 py-16">
        <p class="text-4xl mb-3">🎉</p>
        <p>Không có câu nào sai trong bài này!</p>
      </div>

      <div v-else>
        <p class="text-sm text-gray-500 mb-4">
          {{ store.reviewQuestions.length }} câu cần ôn tập — xem lại đáp án đúng và giải thích bên dưới.
        </p>
        <div class="space-y-4">
          <QuestionCard
            v-for="q in store.reviewQuestions"
            :key="q.id"
            :question="q"
            :interactive="false"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useExamStore } from '@/stores/exam-store'
import QuestionCard from '@/components/QuestionCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const props = defineProps<{ sessionId: number }>()
const store = useExamStore()

onMounted(() => store.fetchReview(props.sessionId))
</script>
