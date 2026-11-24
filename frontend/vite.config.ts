import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath } from 'node:url'
import { resolve } from 'node:path'
import vue from '@vitejs/plugin-vue'

const root = fileURLToPath(new URL('./src', import.meta.url))

export default defineConfig({
  base: '/static/',
  plugins: [tailwindcss(), vue()],
  resolve: {
    alias: { '@': resolve(root, 'src'), '@dashboard': resolve(root, 'src/dashboard') },
  },
  server: {
    port: 5173,
    strictPort: true,
    origin: 'http://localhost:5173',
    cors: true,
  },
  build: {
    outDir: resolve(root, 'dist'),
    emptyOutDir: true,
    manifest: 'manifest.json',
    rollupOptions: {
      input: {
        main: resolve(root, 'src/main.ts'),
        dashboard: resolve(root, 'src/dashboard/main.ts'),
      },
    },
  },
})
