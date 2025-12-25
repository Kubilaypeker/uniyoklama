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
  const token = ref<string | null>(localStorage.getItem("access_token"));

  const isAuthenticated = computed(() => !!token.value);

  async function login(email: string, password: string) {
    const api = await getApi();
    const resp = await api.post("/api/auth/login", { email, password });
    const accessToken = resp.data.access_token;
    localStorage.setItem("access_token", accessToken);
    token.value = accessToken;
    user.value = resp.data.user as User;
  }

  async function fetchMe() {
    const api = await getApi();
    const resp = await api.get("/api/auth/me");
    user.value = resp.data.user as User;
  }

  function logout() {
    localStorage.removeItem("access_token");
    token.value = null;
    user.value = null;
  }

  const role = computed(() => user.value?.role ?? null);

  return { user, role, isAuthenticated, login, fetchMe, logout };
});
