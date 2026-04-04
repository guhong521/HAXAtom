import { createApp } from "vue";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "./styles/theme.css";
import { initSettings } from "./stores/settings";
import router from "./router";

// 初始化设置（语言、深色模式）
initSettings();

const app = createApp(App);
app.use(ElementPlus);
app.use(router);
app.mount("#app");
