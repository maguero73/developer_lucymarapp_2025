import { createApp } from 'vue'
import { createPinia } from 'pinia'
// main.js
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'; 
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')

app.use(createPinia()) 
