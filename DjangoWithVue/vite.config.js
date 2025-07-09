import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss(),],
   server: { // or use your local IP like '192.168.1.10'
    port: 5174       // optional: change port too
  }
})
