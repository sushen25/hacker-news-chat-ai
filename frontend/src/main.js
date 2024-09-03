import { createApp } from "vue";
import App from "./App.vue";
import axiosInstance from "./axios.ts";

const app = createApp(App);

app.config.globalProperties.$axios = axiosInstance;

app.mount("#app");
