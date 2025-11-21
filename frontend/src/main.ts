import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { initState } from './state';

const app = createApp(App);

app.use(router);

app.mount('#app');
initState();