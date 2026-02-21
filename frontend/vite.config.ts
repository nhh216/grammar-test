import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
  // Load env from root directory (one level up from frontend/)
  const env = loadEnv(mode, '../', '')

  const vitePort = parseInt(env.VITE_PORT || '5173')
  const bePort = parseInt(env.BE_PORT || '8000')

  return {
    plugins: [vue(), tailwindcss()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      port: vitePort,
      proxy: {
        // Forward /api/* to FastAPI backend
        '/api': {
          target: `http://localhost:${bePort}`,
          changeOrigin: true,
        },
      },
    },
  }
})
