<!--
  Topic card: navigates to the topic detail/summary page on click.
-->
<template>
  <router-link
    :to="{ name: 'topic', params: { slug: topic.slug } }"
    class="block text-left w-full border rounded-xl p-4 transition-all hover:border-blue-400 hover:shadow-md hover:bg-blue-50 border-gray-200 bg-white"
  >
    <h3 class="font-semibold text-gray-800">{{ topic.name }}</h3>
    <p class="text-sm text-gray-500 mt-1 leading-relaxed">{{ topic.description }}</p>
    <span class="inline-block mt-3 text-xs text-blue-600 font-medium">Xem lý thuyết →</span>
  </router-link>
</template>

<script setup lang="ts">
import type { Topic } from '@/types'
defineProps<{ topic: Topic }>()
</script>
