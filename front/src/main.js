import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ImageUploadVue from 'image-upload-vue'

createApp(App)
.use(router)
.use(ImageUploadVue)
.mount('#app')
