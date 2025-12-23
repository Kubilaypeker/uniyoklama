<template>
  <div class="min-h-screen">
    <div class="navbar bg-base-100 shadow-sm">
      <div class="flex-1">
        <RouterLink class="btn btn-ghost text-xl" to="/">UniYoklama</RouterLink>
      </div>
      <div class="flex-none gap-2" v-if="auth.isAuthenticated">
        <div class="text-sm opacity-80 hidden sm:block">
          <div>{{ auth.user?.full_name || auth.user?.email }}</div>
          <div class="badge badge-outline">{{ auth.user?.role }}</div>
        </div>
        <button class="btn btn-sm" @click="logout">Çıkış</button>
      </div>
      <div v-else class="flex-none">
        <RouterLink class="btn btn-sm" to="/login">Giriş</RouterLink>
      </div>
    </div>

    <main class="max-w-7xl mx-auto p-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "./stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

function logout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>
