import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      // 🎯 When we call /api/v1/... in our code:
      '/api': {
        target: 'http://tennis_api:8000',
        changeOrigin: true,
        // ❌ REMOVE or COMMENT OUT the rewrite line
        // rewrite: (path) => path.replace(/^\/api/, '') 
        
        // 🎯 Now: /api/v1/lab/performance -> http://tennis_api:8000/api/v1/lab/performance
      }
    }
  }
})
