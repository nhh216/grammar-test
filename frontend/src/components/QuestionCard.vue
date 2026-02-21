<!--
  Reusable question card used in ExamView, ResultView, and ReviewView.
  - exam mode: options are clickable, shows selection state
  - review/result mode: shows correct/incorrect highlight + explanation
-->
<template>
  <div class="bg-white rounded-xl border shadow-sm p-5">
    <!-- Question header -->
    <div class="flex items-start gap-3 mb-4">
      <span class="text-xs font-bold bg-blue-600 text-white rounded-full w-7 h-7 flex items-center justify-center shrink-0">
        {{ question.question_number }}
      </span>
      <p class="text-gray-800 font-medium leading-relaxed">{{ question.question_text }}</p>
    </div>

    <!-- Options -->
    <div class="space-y-2">
      <button
        v-for="(text, key) in question.options"
        :key="key"
        class="w-full text-left px-4 py-2.5 rounded-lg border text-sm transition-all"
        :class="optionClass(key)"
        :disabled="!interactive"
        @click="interactive && emit('answer', question.id, key)"
      >
        <span class="font-semibold mr-2">{{ key }}.</span>{{ text }}
      </button>
    </div>

    <!-- Explanation (shown after grading) -->
    <div v-if="question.explanation" class="mt-4 p-3 rounded-lg text-sm leading-relaxed"
      :class="question.is_correct ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'"
    >
      <span class="font-semibold">{{ question.is_correct ? '✓ Đúng! ' : '✗ Sai. ' }}</span>
      {{ question.explanation }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types'

const props = defineProps<{
  question: Question
  selectedAnswer?: string | null
  interactive?: boolean
}>()

const emit = defineEmits<{ answer: [questionId: number, key: string] }>()

function optionClass(key: string): string {
  const selected = props.selectedAnswer === key || props.question.user_answer === key
  const isCorrect = props.question.correct_answer === key
  const hasResult = props.question.correct_answer !== null

  if (hasResult) {
    if (isCorrect) return 'border-green-500 bg-green-50 text-green-800'
    if (selected && !isCorrect) return 'border-red-400 bg-red-50 text-red-700'
    return 'border-gray-200 text-gray-600 cursor-default'
  }

  // Exam mode (no results yet)
  if (selected) return 'border-blue-500 bg-blue-50 text-blue-800 font-medium'
  return 'border-gray-200 text-gray-700 hover:border-blue-300 hover:bg-blue-50'
}
</script>
