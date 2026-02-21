<!--
  Topic detail page: shows full grammar summary and lets user configure + start exam.
-->
<template>
  <div class="max-w-3xl mx-auto px-4 py-6 sm:py-8">
    <!-- Back link -->
    <router-link
      :to="{ name: 'home' }"
      class="inline-flex items-center gap-1.5 text-sm text-blue-600 hover:text-blue-800 mb-6 transition-colors"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
      Quay lại danh sách
    </router-link>

    <LoadingSpinner v-if="loading" message="Đang tải..." />

    <template v-else-if="topic">
      <!-- Topic header -->
      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">{{ topic.name }}</h1>
        <p class="text-gray-500 mt-2">{{ topic.description }}</p>
      </div>

      <!-- Grammar summary -->
      <article
        v-if="topic.summary"
        class="bg-white border border-gray-200 rounded-2xl p-4 sm:p-6 mb-8 prose-content overflow-hidden"
        v-html="renderedSummary"
      />
      <div v-else class="bg-gray-50 rounded-2xl p-6 mb-8 text-gray-400 italic text-sm">
        Chưa có tóm tắt ngữ pháp cho chủ đề này.
      </div>

      <!-- Start exam card -->
      <div class="bg-blue-50 border border-blue-200 rounded-2xl p-6 flex flex-col sm:flex-row items-start sm:items-center gap-6">
        <div class="flex-1 w-full">
          <p class="text-sm font-semibold text-blue-800 mb-3">Chọn số câu hỏi</p>
          <div class="flex gap-3">
            <button
              v-for="n in [5, 10, 15, 20]"
              :key="n"
              class="flex-1 py-2 rounded-lg border-2 font-semibold text-sm transition-all"
              :class="numQuestions === n
                ? 'border-blue-600 bg-blue-600 text-white'
                : 'border-blue-200 bg-white text-blue-700 hover:border-blue-400'"
              @click="numQuestions = n"
            >
              {{ n }} câu
            </button>
          </div>
        </div>
        <button
          class="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors w-full sm:w-auto disabled:opacity-40"
          :disabled="store.loading"
          @click="startExam"
        >
          {{ store.loading ? 'Đang tạo đề...' : 'Làm đề →' }}
        </button>
      </div>

      <div v-if="store.error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
        {{ store.error }}
        <button class="ml-2 underline" @click="store.clearError">Đóng</button>
      </div>
    </template>

    <div v-else class="text-center py-16 text-gray-400">Không tìm thấy chủ đề.</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExamStore } from '@/stores/exam-store'
import type { Topic } from '@/types'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { renderMarkdown } from '@/utils/markdown-renderer'

const props = defineProps<{ slug: string }>()
const store = useExamStore()
const router = useRouter()
const numQuestions = ref(10)
const loading = ref(false)

const topic = computed<Topic | undefined>(() =>
  store.topics.find(t => t.slug === props.slug)
)

const renderedSummary = computed(() =>
  topic.value?.summary ? renderMarkdown(topic.value.summary) : ''
)

onMounted(async () => {
  if (!store.topics.length) {
    loading.value = true
    await store.fetchTopics()
    loading.value = false
  }
})

async function startExam() {
  if (!topic.value) return
  const sessionId = await store.startExam(topic.value.id, numQuestions.value)
  if (sessionId) router.push({ name: 'exam', params: { sessionId } })
}
</script>
