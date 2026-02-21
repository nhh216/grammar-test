<template>
  <div class="flex flex-col items-center justify-center py-16 gap-4">
    <div class="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
    <p class="text-gray-500 text-sm">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ message?: string }>(), {
  message: 'Đang tải...',
})
</script>
