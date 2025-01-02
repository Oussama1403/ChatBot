import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import LoginPage from './components/LoginPage.vue';
import SignupPage from './components/SignupPage.vue';
import ChatPage from './components/ChatPage.vue';
import router from './router'; // Import the router instance



createApp(App).use(router).mount('#app');
