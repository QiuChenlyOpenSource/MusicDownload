import { createSSRApp } from "vue";

import element from "element-plus";

import "element-plus/dist/index.css";
import "element-plus/theme-chalk/dark/css-vars.css";
import "./style.css";

import App from "./App.vue";

import router from "./router/router";
import { createPinia } from "pinia";
import persist from "pinia-plugin-persistedstate";

const app = createSSRApp(App);
const pinia = createPinia();
pinia.use(persist);

app.use(router);
app.use(pinia);
app.use(element);
app.mount("#app");
