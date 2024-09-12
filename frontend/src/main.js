import { createApp } from "vue";
import App from "./App.vue";
import axiosInstance from "./axios.ts";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap';

const app = createApp(App);

app.config.globalProperties.$axios = axiosInstance;

app.mount("#app");
