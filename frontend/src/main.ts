import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router";
import App from "./App.vue";
import "./style.css";
import { useAuthStore } from "./stores/auth";

const app = createApp(App);
app.use(createPinia());
app.use(router);

router.isReady().then(async () => {
  const auth = useAuthStore();
  if (localStorage.getItem("access_token")) {
    try {
      await auth.fetchMe();
    } catch {
      auth.logout();
    }
  }
  app.mount("#app");
});
