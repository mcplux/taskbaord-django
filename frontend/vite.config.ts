import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath } from 'node:url'
import { resolve } from 'node:path'

export default defineConfig({
  base: '/static/',
  plugins: [tailwindcss()],
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
