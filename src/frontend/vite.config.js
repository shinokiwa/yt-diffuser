import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: true,
    // Dockerのバインドマウントでは監視が働かないっぽいのでプーリングを使う
    watch: {
      usePolling: true,
      interval: 1000
    }
  }
})
