<!--
  Performance analytics page: per-topic accuracy, level classification, trend, and AI coaching insights.
-->
<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Phân tích năng lực</h1>
      <p class="text-gray-500 mt-2">Đánh giá điểm mạnh, điểm yếu và gợi ý cải thiện</p>
    </div>

    <LoadingSpinner v-if="loadingPerf" message="Đang tải dữ liệu..." />

    <template v-else-if="perf">
      <!-- No data state -->
      <div v-if="!perf.has_data" class="text-center py-16 bg-white rounded-2xl border border-gray-200">
        <div class="text-5xl mb-4">📊</div>
        <h2 class="text-xl font-semibold text-gray-700 mb-2">Chưa có dữ liệu</h2>
        <p class="text-gray-500 mb-6">Hoàn thành ít nhất một bài thi để xem phân tích năng lực</p>
        <router-link
          :to="{ name: 'home' }"
          class="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          Bắt đầu luyện thi →
        </router-link>
      </div>

      <template v-else>
        <!-- Summary cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
          <div class="bg-white rounded-xl border border-gray-200 p-4 text-center">
            <div class="text-2xl font-bold text-blue-600">{{ perf.total_sessions }}</div>
            <div class="text-xs text-gray-500 mt-1">Bài đã làm</div>
          </div>
          <div class="bg-white rounded-xl border border-gray-200 p-4 text-center">
            <div class="text-2xl font-bold text-gray-800">{{ perf.total_questions_answered }}</div>
            <div class="text-xs text-gray-500 mt-1">Câu hỏi</div>
          </div>
          <div class="bg-white rounded-xl border border-gray-200 p-4 text-center">
            <div class="text-2xl font-bold" :class="accuracyColor(perf.overall_accuracy)">
              {{ perf.overall_accuracy }}%
            </div>
            <div class="text-xs text-gray-500 mt-1">Độ chính xác</div>
          </div>
          <div class="bg-white rounded-xl border border-gray-200 p-4 text-center">
            <div class="text-2xl font-bold text-gray-800">
              {{ testedCount }}/{{ perf.topics.length }}
            </div>
            <div class="text-xs text-gray-500 mt-1">Chủ đề đã học</div>
          </div>
        </div>

        <!-- AI Insights -->
        <div class="bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl p-6 mb-8 text-white">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold">🤖 Đánh giá từ AI Coach</h2>
            <button
              class="text-xs bg-white/20 hover:bg-white/30 px-3 py-1.5 rounded-lg transition-colors font-medium"
              :disabled="loadingInsights"
              @click="loadInsights"
            >
              {{ loadingInsights ? 'Đang phân tích...' : '↻ Làm mới' }}
            </button>
          </div>

          <div v-if="loadingInsights" class="text-blue-100 text-sm animate-pulse">
            AI đang phân tích dữ liệu của bạn...
          </div>

          <template v-else-if="insights">
            <!-- Level badge + summary -->
            <div class="flex items-start gap-3 mb-4">
              <span class="bg-white/20 text-white text-sm font-semibold px-3 py-1 rounded-full whitespace-nowrap">
                {{ insights.overall_level }}
              </span>
              <p class="text-blue-50 text-sm leading-relaxed">{{ insights.summary }}</p>
            </div>

            <div class="grid sm:grid-cols-2 gap-4">
              <!-- Weak topics -->
              <div v-if="insights.weak_topics.length" class="bg-white/10 rounded-xl p-4">
                <h3 class="text-sm font-semibold mb-2">⚠️ Cần cải thiện</h3>
                <ul class="space-y-1">
                  <li
                    v-for="t in insights.weak_topics"
                    :key="t"
                    class="text-xs text-blue-100 flex items-center gap-1.5"
                  >
                    <span class="w-1.5 h-1.5 bg-red-300 rounded-full flex-shrink-0"></span>
                    {{ t }}
                  </li>
                </ul>
              </div>

              <!-- Strong topics -->
              <div v-if="insights.strong_topics.length" class="bg-white/10 rounded-xl p-4">
                <h3 class="text-sm font-semibold mb-2">✅ Điểm mạnh</h3>
                <ul class="space-y-1">
                  <li
                    v-for="t in insights.strong_topics"
                    :key="t"
                    class="text-xs text-blue-100 flex items-center gap-1.5"
                  >
                    <span class="w-1.5 h-1.5 bg-green-300 rounded-full flex-shrink-0"></span>
                    {{ t }}
                  </li>
                </ul>
              </div>
            </div>

            <!-- Recommendations -->
            <div v-if="insights.recommendations.length" class="mt-4 bg-white/10 rounded-xl p-4">
              <h3 class="text-sm font-semibold mb-2">💡 Gợi ý học tập</h3>
              <ul class="space-y-2">
                <li
                  v-for="(rec, i) in insights.recommendations"
                  :key="i"
                  class="text-xs text-blue-100 flex items-start gap-2"
                >
                  <span class="font-bold text-white mt-0.5">{{ i + 1 }}.</span>
                  <span>{{ rec }}</span>
                </li>
              </ul>
            </div>

            <!-- Study plan -->
            <div v-if="insights.study_plan" class="mt-4 bg-white/10 rounded-xl p-4">
              <h3 class="text-sm font-semibold mb-1">📅 Lộ trình đề xuất</h3>
              <p class="text-xs text-blue-100 leading-relaxed">{{ insights.study_plan }}</p>
            </div>
          </template>

          <div v-else-if="insightsError" class="text-red-200 text-sm">
            {{ insightsError }}
            <button class="ml-2 underline" @click="loadInsights">Thử lại</button>
          </div>
        </div>

        <!-- Topic breakdown -->
        <div class="bg-white rounded-2xl border border-gray-200 overflow-hidden">
          <div class="px-4 sm:px-6 py-4 border-b border-gray-100">
            <div class="flex items-center justify-between gap-2">
              <h2 class="font-semibold text-gray-800 shrink-0">Chi tiết theo chủ đề</h2>
              <div class="flex gap-2 sm:gap-3 text-xs text-gray-500">
                <span class="flex items-center gap-1"><span class="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-red-400 inline-block flex-shrink-0"></span><span class="hidden sm:inline">Yếu &lt;60%</span><span class="sm:hidden">&lt;60</span></span>
                <span class="flex items-center gap-1"><span class="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-yellow-400 inline-block flex-shrink-0"></span><span class="hidden sm:inline">TB 60-79%</span><span class="sm:hidden">60-79</span></span>
                <span class="flex items-center gap-1"><span class="w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-green-500 inline-block flex-shrink-0"></span><span class="hidden sm:inline">Tốt ≥80%</span><span class="sm:hidden">≥80</span></span>
              </div>
            </div>
          </div>

          <div class="divide-y divide-gray-50">
            <div
              v-for="topic in sortedTopics"
              :key="topic.topic_id"
              class="px-4 sm:px-6 py-3 sm:py-4 hover:bg-gray-50 transition-colors"
            >
              <div class="flex items-center gap-3">
                <!-- Level dot -->
                <span
                  class="w-2.5 h-2.5 rounded-full flex-shrink-0"
                  :class="levelDotClass(topic.level)"
                ></span>

                <!-- Topic name + stats -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1.5 gap-2">
                    <div class="flex items-center gap-1.5 min-w-0">
                      <span class="text-sm font-medium text-gray-800 truncate">{{ topic.topic_name }}</span>
                      <span class="text-xs px-1.5 py-0.5 rounded-full font-medium flex-shrink-0" :class="levelBadgeClass(topic.level)">
                        {{ levelLabel(topic.level) }}
                      </span>
                      <span v-if="topic.trend !== 'new' && topic.trend !== 'stable'" class="text-xs flex-shrink-0" :title="trendLabel(topic.trend)">
                        {{ topic.trend === 'improving' ? '↑' : '↓' }}
                      </span>
                    </div>
                    <span class="text-sm font-semibold text-gray-700 flex-shrink-0">
                      {{ topic.sessions_completed === 0 ? '—' : topic.accuracy_pct + '%' }}
                    </span>
                  </div>

                  <!-- Progress bar -->
                  <div class="w-full bg-gray-100 rounded-full h-1.5">
                    <div
                      class="h-1.5 rounded-full transition-all duration-500"
                      :class="levelBarClass(topic.level)"
                      :style="{ width: topic.sessions_completed === 0 ? '0%' : topic.accuracy_pct + '%' }"
                    ></div>
                  </div>

                  <!-- Sub stats -->
                  <div class="flex flex-wrap items-center gap-x-3 gap-y-0.5 mt-1 text-xs text-gray-400">
                    <span v-if="topic.sessions_completed === 0">Chưa làm bài</span>
                    <template v-else>
                      <span>{{ topic.sessions_completed }} bài</span>
                      <span>{{ topic.total_correct }}/{{ topic.total_questions }} đúng</span>
                      <span v-if="topic.trend !== 'new'" :class="topic.trend === 'improving' ? 'text-green-500' : topic.trend === 'declining' ? 'text-red-400' : 'text-gray-400'">
                        {{ trendLabel(topic.trend) }}
                      </span>
                    </template>
                  </div>
                </div>

                <!-- Practice button -->
                <router-link
                  :to="{ name: 'topic', params: { slug: topic.slug } }"
                  class="flex-shrink-0 text-xs text-blue-600 hover:text-blue-800 font-medium border border-blue-200 hover:border-blue-400 px-2 py-1 rounded-lg transition-colors"
                >
                  Luyện →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api } from '@/services/api'
import type { PerformanceResponse, PerformanceInsight, TopicPerformance } from '@/types'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const perf = ref<PerformanceResponse | null>(null)
const insights = ref<PerformanceInsight | null>(null)
const loadingPerf = ref(true)
const loadingInsights = ref(false)
const insightsError = ref<string | null>(null)

const testedCount = computed(() =>
  perf.value?.topics.filter(t => t.sessions_completed > 0).length ?? 0
)

// Sort: weak first, then moderate, then untested, then strong
const sortedTopics = computed<TopicPerformance[]>(() => {
  if (!perf.value) return []
  const order = { weak: 0, moderate: 1, untested: 2, strong: 3 }
  return [...perf.value.topics].sort((a, b) => {
    const diff = order[a.level] - order[b.level]
    if (diff !== 0) return diff
    return a.accuracy_pct - b.accuracy_pct
  })
})

onMounted(async () => {
  try {
    perf.value = await api.getPerformance()
    if (perf.value.has_data) loadInsights()
  } catch (e: unknown) {
    console.error(e)
  } finally {
    loadingPerf.value = false
  }
})

async function loadInsights() {
  loadingInsights.value = true
  insightsError.value = null
  try {
    insights.value = await api.getInsights()
  } catch (e: unknown) {
    insightsError.value = e instanceof Error ? e.message : 'Không thể tải đánh giá AI.'
  } finally {
    loadingInsights.value = false
  }
}

function accuracyColor(pct: number) {
  if (pct >= 80) return 'text-green-600'
  if (pct >= 60) return 'text-yellow-600'
  return 'text-red-500'
}

function levelDotClass(level: string) {
  return {
    weak: 'bg-red-400',
    moderate: 'bg-yellow-400',
    strong: 'bg-green-500',
    untested: 'bg-gray-300',
  }[level] ?? 'bg-gray-300'
}

function levelBarClass(level: string) {
  return {
    weak: 'bg-red-400',
    moderate: 'bg-yellow-400',
    strong: 'bg-green-500',
    untested: 'bg-gray-200',
  }[level] ?? 'bg-gray-200'
}

function levelBadgeClass(level: string) {
  return {
    weak: 'bg-red-100 text-red-700',
    moderate: 'bg-yellow-100 text-yellow-700',
    strong: 'bg-green-100 text-green-700',
    untested: 'bg-gray-100 text-gray-500',
  }[level] ?? 'bg-gray-100 text-gray-500'
}

function levelLabel(level: string) {
  return { weak: 'Yếu', moderate: 'Trung bình', strong: 'Tốt', untested: 'Chưa học' }[level] ?? level
}

function trendLabel(trend: string) {
  return { improving: 'Đang tiến bộ', declining: 'Có dấu hiệu giảm', stable: 'Ổn định', new: '' }[trend] ?? ''
}
</script>
