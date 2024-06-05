import { createRouter, createWebHistory } from 'vue-router';
import ConfigurationForm from './components/ConfigurationForm.vue';
import UploadOptions from './components/UploadOptions.vue';
import UploadFiles from './components/UploadFiles.vue';
import TakePhotos from './components/TakePhotos.vue';
import ModelView from './components/ModelView.vue';

const routes = [
  { path: '/', component: ConfigurationForm },
  { path: '/upload-options', component: UploadOptions },
  { path: '/upload-files', component: UploadFiles },
  { path: '/take-photos', component: TakePhotos },
  { path: '/model-view', component: ModelView }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
