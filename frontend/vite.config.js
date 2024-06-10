import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv'

// Load environment variables from .env file
dotenv.config()

export default defineConfig({
  plugins: [vue({
    template: {
      compilerOptions: {
        isCustomElement: (tag) => tag === 'model-viewer'
      }
    }
  })],
  define: {
    'process.env': process.env
  },
  server: {
    host: '0.0.0.0'
  }
})
