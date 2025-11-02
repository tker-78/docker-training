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
import keycloak from './keycloak'

// Styles
import 'unfonts.css'

const app = createApp(App)
registerPlugins(app)

keycloak.init({ onLoad: 'login-required' }).then((authenticated: boolean) => {
  if (authenticated) {
    app.config.globalProperties.$keycloak = keycloak
    app.mount('#app')
  } else {
    window.location.reload()
  }
})
