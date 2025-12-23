import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { getApi } from "../lib/api";

export type User = {
  id: number;
  email: string;
  full_name: string;
  role: "ADMIN" | "STAFF" | "INSTRUCTOR" | "STUDENT";
};

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const isAuthenticated = computed(() => !!localStorage.getItem("access_token"));

  async function login(email: string, password: string) {
    const api = await getApi();
    const resp = await api.post("/api/auth/login", { email, password });
    localStorage.setItem("access_token", resp.data.access_token);
    user.value = resp.data.user as User;
  }

  async function fetchMe() {
    const api = await getApi();
    const resp = await api.get("/api/auth/me");
    user.value = resp.data.user as User;
  }

  function logout() {
    localStorage.removeItem("access_token");
    user.value = null;
  }

  const role = computed(() => user.value?.role ?? null);

  return { user, role, isAuthenticated, login, fetchMe, logout };
});
