import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath } from 'node:url'
import { resolve } from 'node:path'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/static/',
  plugins: [tailwindcss(), vue()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: {
    port: 5173,
    strictPort: true,
    origin: 'http://localhost:5173',
    cors: true,
  },
  build: {
    outDir: resolve(import.meta.dirname, 'dist'),
    manifest: 'manifest.json',
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, 'src/main.ts'),
      },
    },
  },
})
