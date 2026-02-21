<!--
  History page: list all past exam sessions with score and actions.
-->
<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Lịch sử bài thi</h1>

    <LoadingSpinner v-if="store.loading" message="Đang tải lịch sử..." />

    <template v-else>
      <div v-if="store.history.length === 0" class="text-center text-gray-400 py-16">
        <p class="text-4xl mb-3">📋</p>
        <p>Chưa có bài thi nào. <RouterLink to="/" class="text-blue-600 underline">Bắt đầu thi ngay!</RouterLink></p>
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="item in store.history"
          :key="item.id"
          class="bg-white border rounded-xl p-3 sm:p-4 flex items-center justify-between gap-3 shadow-sm hover:border-blue-300 transition-colors"
        >
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-gray-800 truncate">{{ item.topic }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ formatDate(item.created_at) }}</p>
          </div>

          <div class="text-center shrink-0">
            <span class="text-lg font-bold" :class="scoreColor(item)">
              {{ item.score ?? '—' }}/{{ item.total }}
            </span>
            <p class="text-xs text-gray-400">điểm</p>
          </div>

          <div class="flex flex-col xs:flex-row gap-1.5 shrink-0">
            <RouterLink
              :to="{ name: 'result', params: { sessionId: item.id } }"
              class="text-xs sm:text-sm px-2.5 sm:px-3 py-1.5 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 text-center"
            >
              Xem
            </RouterLink>
            <RouterLink
              v-if="item.status === 'completed' && (item.score ?? 0) < item.total"
              :to="{ name: 'review', params: { sessionId: item.id } }"
              class="text-xs sm:text-sm px-2.5 sm:px-3 py-1.5 rounded-lg bg-orange-500 text-white hover:bg-orange-600 text-center"
            >
              Ôn tập
            </RouterLink>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useExamStore } from '@/stores/exam-store'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import type { ExamHistoryItem } from '@/types'

const store = useExamStore()

onMounted(() => store.fetchHistory())

function scoreColor(item: ExamHistoryItem): string {
  if (item.score === null) return 'text-gray-400'
  const pct = item.score / item.total
  if (pct >= 0.8) return 'text-green-600'
  if (pct >= 0.5) return 'text-yellow-600'
  return 'text-red-500'
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
