<template>
  <nav class="bg-blue-600 text-white shadow-md">
    <div class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
      <RouterLink to="/" class="text-xl font-bold tracking-tight hover:opacity-90">
        🎯 TOEIC Grammar
      </RouterLink>

      <!-- Desktop nav -->
      <div class="hidden sm:flex gap-4 text-sm font-medium">
        <RouterLink to="/" class="hover:underline underline-offset-4" active-class="underline">
          Luyện thi
        </RouterLink>
        <RouterLink to="/performance" class="hover:underline underline-offset-4" active-class="underline">
          Phân tích
        </RouterLink>
        <RouterLink to="/history" class="hover:underline underline-offset-4" active-class="underline">
          Lịch sử
        </RouterLink>
      </div>

      <!-- Mobile hamburger button -->
      <button
        class="sm:hidden p-1.5 rounded-lg hover:bg-blue-500 transition-colors"
        :aria-expanded="menuOpen"
        aria-label="Menu"
        @click="menuOpen = !menuOpen"
      >
        <svg v-if="!menuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Mobile dropdown menu -->
    <div v-if="menuOpen" class="sm:hidden border-t border-blue-500 bg-blue-700">
      <RouterLink
        to="/"
        class="block px-4 py-3 text-sm font-medium hover:bg-blue-600 transition-colors"
        active-class="bg-blue-500"
        @click="menuOpen = false"
      >
        🏠 Luyện thi
      </RouterLink>
      <RouterLink
        to="/performance"
        class="block px-4 py-3 text-sm font-medium hover:bg-blue-600 transition-colors"
        active-class="bg-blue-500"
        @click="menuOpen = false"
      >
        📊 Phân tích
      </RouterLink>
      <RouterLink
        to="/history"
        class="block px-4 py-3 text-sm font-medium hover:bg-blue-600 transition-colors"
        active-class="bg-blue-500"
        @click="menuOpen = false"
      >
        📋 Lịch sử
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const menuOpen = ref(false)
</script>
