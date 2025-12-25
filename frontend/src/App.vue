<template>
  <!-- Login page: full screen without navbar -->
  <div v-if="route.name === 'login'">
    <RouterView />
  </div>

  <!-- Other pages: with navbar -->
  <div v-else class="min-h-screen">
    <div class="navbar bg-base-100 shadow-sm px-4 md:px-6">
      <div class="flex-1">
        <RouterLink class="flex items-center gap-2 text-xl font-semibold text-gray-800 hover:text-primary transition-colors" to="/">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
          </svg>
          <span class="hidden md:inline">Selçuk Üniversitesi Yoklama</span>
          <span class="md:hidden">Selçuk Ü. Yoklama</span>
        </RouterLink>
      </div>
      <div class="flex-none flex items-center gap-4" v-if="auth.isAuthenticated">
        <div class="text-sm text-right hidden sm:block">
          <div class="font-medium text-gray-700">{{ auth.user?.full_name || auth.user?.email }}</div>
          <div class="badge badge-outline badge-sm mt-0.5">{{ auth.user?.role }}</div>
        </div>
        <div class="w-px h-8 bg-gray-200 hidden sm:block"></div>
        <button class="btn btn-sm btn-ghost text-gray-600 hover:text-red-500 hover:bg-red-50" @click="logout">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span class="hidden sm:inline">Çıkış</span>
        </button>
      </div>
      <div v-else class="flex-none">
        <RouterLink class="btn btn-sm btn-primary" to="/login">Giriş</RouterLink>
      </div>
    </div>

    <main class="max-w-7xl mx-auto p-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "./stores/auth";
import { useRouter, useRoute } from "vue-router";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

function logout() {
  auth.logout();
  router.push({ name: "login" });
}
</script>

