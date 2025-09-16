import { createApp } from 'vue'
import App from './App.vue'

// Configure feature flags
window.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = false

createApp(App).mount('#app')
