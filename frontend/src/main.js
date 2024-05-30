import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const app = createApp(App)

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import router from './router'
app.use(router)

import store from './store';
app.use(store)

app.mount('#app')
