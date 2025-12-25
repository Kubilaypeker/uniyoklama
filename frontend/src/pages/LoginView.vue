<template>
  <div class="min-h-screen login-bg flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Decorative floating shapes -->
    <div class="floating-shape bg-primary w-64 h-64 -top-32 -left-32" style="animation-delay: 0s;"></div>
    <div class="floating-shape bg-secondary w-48 h-48 top-1/4 -right-24" style="animation-delay: 2s;"></div>
    <div class="floating-shape bg-accent w-32 h-32 bottom-1/4 left-1/4" style="animation-delay: 4s;"></div>

    <!-- Login Card -->
    <div class="glass-card rounded-3xl w-full max-w-md p-8 relative z-10">
      <!-- Header -->
      <div class="text-center mb-8">
        <!-- University Icon -->
        <div class="w-20 h-20 mx-auto mb-4 bg-primary/10 rounded-2xl flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mb-1">Selçuk Üniversitesi</h1>
        <p class="text-gray-500 text-sm">Online Yoklama Sistemi</p>
      </div>

      <!-- Error Alert -->
      <div v-if="errorMsg" class="alert alert-warning mb-6 rounded-xl">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-5 w-5" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span class="text-sm">{{ errorMsg }}</span>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="onLogin" class="space-y-5">
        <!-- Email Input -->
        <div class="form-control">
          <label class="label pb-1">
            <span class="label-text font-medium text-gray-700">E-posta Adresi</span>
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
              </svg>
            </div>
            <input 
              v-model="email" 
              type="email" 
              placeholder="ornek@selcuk.edu.tr" 
              class="input login-input w-full pl-12 h-12 rounded-xl focus:outline-none"
              required
            />
          </div>
        </div>

        <!-- Password Input -->
        <div class="form-control">
          <label class="label pb-1">
            <span class="label-text font-medium text-gray-700">Şifre</span>
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <input 
              v-model="password" 
              :type="showPassword ? 'text' : 'password'" 
              placeholder="••••••••" 
              class="input login-input w-full pl-12 pr-12 h-12 rounded-xl focus:outline-none"
              required
            />
            <!-- Password Toggle Button -->
            <button 
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
            >
              <!-- Eye Open Icon -->
              <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <!-- Eye Closed Icon -->
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Login Button -->
        <button 
          type="submit" 
          class="btn btn-primary login-btn w-full h-12 rounded-xl text-base mt-2" 
          :disabled="loading"
        >
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          <span v-else>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
            Giriş Yap
          </span>
        </button>
      </form>

      <!-- Demo Info -->
      <div class="mt-6 pt-6 border-t border-gray-100">
        <p class="text-xs text-gray-400 text-center mb-3">Demo Hesapları</p>
        <div class="grid grid-cols-2 gap-3 text-xs">
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <div class="font-semibold text-gray-600 mb-1">Öğretim Görevlisi</div>
            <code class="text-primary text-[10px]">instructor@demo.com</code>
          </div>
          <div class="bg-gray-50 rounded-lg p-3 text-center">
            <div class="font-semibold text-gray-600 mb-1">Öğrenci</div>
            <code class="text-primary text-[10px]">student@demo.com</code>
          </div>
        </div>
        <p class="text-[10px] text-gray-400 text-center mt-2">Şifre: <code>demo1234</code></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMsg = ref<string | null>(null);

async function onLogin() {
  errorMsg.value = null;
  loading.value = true;
  try {
    await auth.login(email.value, password.value);
    const next = typeof route.query.next === "string" ? route.query.next : "/";
    router.push(next);
  } catch (e: any) {
    // Tüm hata durumlarında tutarlı mesaj
    const status = e?.response?.status;
    
    if (status === 401 || status === 400) {
      errorMsg.value = "E-posta veya şifre hatalı. Lütfen bilgilerinizi kontrol edin.";
    } else if (status === 404) {
      errorMsg.value = "Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı.";
    } else if (e?.code === "ERR_NETWORK" || e?.message?.includes("Network") || !e?.response) {
      errorMsg.value = "Sunucuya bağlanılamadı. Lütfen internet bağlantınızı kontrol edin.";
    } else {
      errorMsg.value = "Giriş başarısız. Lütfen bilgilerinizi kontrol edip tekrar deneyin.";
    }
  } finally {
    loading.value = false;
  }
}
</script>
