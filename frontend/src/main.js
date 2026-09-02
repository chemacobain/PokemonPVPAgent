import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useTeamStore } from './stores/teamStore'
import './assets/styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

const teamStore = useTeamStore(pinia)
teamStore.setLeague('1500')

app.mount('#app')
