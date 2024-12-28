import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);
app.use(router); // Make sure router is added to Vue instance
app.mount("#app");
