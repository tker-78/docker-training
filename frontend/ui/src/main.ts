/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
// Styles
import 'unfonts.css'

const app = createApp(App)
registerPlugins(app)

const backendOrigin =
  import.meta.env.VITE_BACKEND_ORIGIN ?? 'http://localhost:8000'

const cookies = document.cookie.split(';').map((item) => item.trim())
const hasAccessToken = cookies.some((cookie) => cookie.startsWith('access_token='))

if (!hasAccessToken) {
  const loginUrl = new URL('/auth/login', backendOrigin)
  loginUrl.searchParams.set('redirect', window.location.href)
  window.location.href = loginUrl.toString()
} else {
  app.mount('#app')
}
