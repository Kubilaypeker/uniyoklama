<template>
  <div class="flex justify-center">
    <div class="card w-full max-w-md bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Giriş</h2>

        <div class="alert alert-warning" v-if="errorMsg">
          <span>{{ errorMsg }}</span>
        </div>

        <label class="form-control w-full">
          <div class="label"><span class="label-text">E-posta</span></div>
          <input v-model="email" type="email" placeholder="ornek@uni.edu" class="input input-bordered w-full" />
        </label>

        <label class="form-control w-full">
          <div class="label"><span class="label-text">Şifre</span></div>
          <input v-model="password" type="password" placeholder="••••••••" class="input input-bordered w-full" />
        </label>

        <div class="card-actions justify-end mt-2">
          <button class="btn btn-primary" :disabled="loading" @click="onLogin">
            <span v-if="loading" class="loading loading-spinner loading-sm"></span>
            Giriş Yap
          </button>
        </div>

        <div class="text-xs opacity-70 mt-4">
          Demo: <code>instructor@demo.com</code> / <code>demo1234</code> veya <code>student@demo.com</code> / <code>demo1234</code>
        </div>
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
    const msg =
      e?.response?.data?.details ||
      e?.response?.data?.error ||
      e?.message ||
      "Giriş başarısız.";
    errorMsg.value = String(msg);
  } finally {
    loading.value = false;
  }
}
</script>
