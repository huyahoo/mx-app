import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import "https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js";
import '@fortawesome/fontawesome-free/css/all.css';

const app = createApp(App)

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import router from './router'
app.use(router)

import store from './store';
app.use(store)

app.mount('#app')
