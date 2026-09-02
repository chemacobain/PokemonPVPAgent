import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useTeamStore } from './stores/teamStore'
import './assets/styles/main.css'

import VueGtag from 'vue-gtag'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize Google Analytics if an ID is provided
if (import.meta.env.VITE_GA_ID) {
  app.use(VueGtag, {
    config: { id: import.meta.env.VITE_GA_ID }
  }, router)
}

const teamStore = useTeamStore(pinia)
teamStore.setLeague('1500')

app.mount('#app')
