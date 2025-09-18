import { fileURLToPath, URL } from 'node:url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueDevTools from 'vite-plugin-vue-devtools';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@api': fileURLToPath(new URL('./src/api', import.meta.url))
    }
  },
  define: {
    'import.meta.env.VERCEL_ENV': JSON.stringify(process.env.VERCEL_ENV),
    'import.meta.env.VERCEL_RELATED_PROJECTS': JSON.stringify(process.env.VERCEL_RELATED_PROJECTS)
  }
});
