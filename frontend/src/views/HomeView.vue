<!--
  Home page: topic grid. Click a topic to view its grammar summary page.
-->
<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Luyện thi TOEIC Grammar</h1>
      <p class="text-gray-500 mt-2">Chọn chủ đề để ôn lý thuyết và làm đề</p>
    </div>

    <LoadingSpinner v-if="store.loading" message="Đang tải..." />

    <template v-else>
      <div v-if="store.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
        {{ store.error }}
        <button class="ml-2 underline" @click="store.clearError">Đóng</button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <TopicCard
          v-for="topic in store.topics"
          :key="topic.id"
          :topic="topic"
        />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useExamStore } from '@/stores/exam-store'
import TopicCard from '@/components/TopicCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const store = useExamStore()
onMounted(() => store.fetchTopics())
</script>
