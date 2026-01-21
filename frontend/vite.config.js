import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      '/chat': 'http://localhost:8000',
      '/knowledge': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
      '/search': 'http://localhost:8000'
    }
  }
})
