import { createApp } from "vue";
import App from "./App.vue";
import axiosInstance from "./axios.ts";
import router from "./router/router.ts";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap';

const app = createApp(App);
app.use(router);

app.config.globalProperties.$axios = axiosInstance;

app.mount("#app");
