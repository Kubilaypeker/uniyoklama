<template>
  <div class="space-y-6">
    <div v-if="auth.user?.role !== 'INSTRUCTOR'" class="alert alert-error rounded-xl shadow-sm">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>Bu sayfa sadece öğretim görevlileri içindir.</span>
    </div>

    <div v-else class="space-y-6">
      <!-- Error Alert -->
      <div v-if="errorMsg" class="alert alert-warning rounded-xl shadow-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span>{{ errorMsg }}</span>
      </div>

      <!-- Main Session Card -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <!-- Header -->
        <div class="px-6 py-5 border-b border-gray-100 bg-gradient-to-r from-primary/5 to-transparent">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div class="flex items-center gap-4">
              <div 
                class="w-14 h-14 rounded-2xl flex items-center justify-center shrink-0"
                :class="session?.is_open ? 'bg-green-100' : 'bg-gray-100'"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-7 w-7" 
                  :class="session?.is_open ? 'text-green-600' : 'text-gray-500'" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path v-if="session?.is_open" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <div>
                <div class="flex items-center gap-3 flex-wrap">
                  <h2 class="text-xl font-bold text-gray-800">Oturum #{{ sessionId }}</h2>
                  <span 
                    class="badge gap-1 px-3 py-2"
                    :class="session?.is_open ? 'badge-success text-white' : 'badge-ghost'"
                  >
                    <svg v-if="session?.is_open" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    {{ session?.is_open ? "Açık" : "Kapalı" }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mt-1">
                  {{ session?.course_code }} - {{ session?.course_title }}
                </p>
                <p class="text-xs text-gray-500 mt-0.5">
                  {{ session?.term_code }} / Şube {{ session?.section }}
                </p>
              </div>
            </div>

            <div class="flex flex-wrap gap-2">
              <button 
                class="btn btn-success gap-2" 
                :disabled="loading || session?.is_open" 
                @click="toggleOpen(true)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                </svg>
                Aç
              </button>
              <button 
                class="btn btn-warning gap-2" 
                :disabled="loading || !session?.is_open" 
                @click="toggleOpen(false)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                Kapat
              </button>
              <button class="btn btn-primary gap-2" :disabled="loading" @click="refreshAll">
                <span v-if="loading" class="loading loading-spinner loading-sm"></span>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Yenile
              </button>
            </div>
          </div>

          <!-- Time Info -->
          <div class="mt-4 flex items-center gap-4 flex-wrap">
            <div class="flex items-center gap-2 bg-white/60 backdrop-blur-sm rounded-xl px-4 py-2 border border-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-sm text-gray-700">
                <span class="font-medium">{{ session?.starts_at }}</span>
                <span class="text-gray-400 mx-2">→</span>
                <span class="font-medium">{{ session?.ends_at }}</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="p-6">
          <div class="grid gap-6 md:grid-cols-2">
            <!-- QR Card -->
            <div class="bg-gray-50 rounded-xl border border-gray-100 overflow-hidden">
              <div class="px-4 py-3 border-b border-gray-100 bg-white">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                  </svg>
                  <h3 class="font-semibold text-gray-800">QR Kodu</h3>
                </div>
              </div>

              <div class="p-4">
                <div v-if="qrError" class="alert alert-warning rounded-lg mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <span class="text-sm">{{ qrError }}</span>
                </div>

                <div v-if="qr?.image_data_url" class="flex flex-col items-center gap-4">
                  <div class="bg-white rounded-2xl p-4 shadow-sm border border-gray-100">
                    <img :src="qr.image_data_url" alt="QR" class="w-full max-w-[240px]" />
                  </div>

                  <div class="text-center space-y-2">
                    <div class="flex items-center justify-center gap-2 text-sm">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>QR süresi: <b class="text-primary">{{ qr.expires_in }}</b> saniye</span>
                    </div>
                    <p class="text-xs text-gray-500">Öğrenciler bu QR'ı okutarak <code class="bg-gray-100 px-1 py-0.5 rounded">/scan</code> ekranına gider</p>
                  </div>

                  <button class="btn btn-primary btn-sm gap-2" @click="refreshQr">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    QR Yenile
                  </button>
                </div>

                <div v-else class="py-12 text-center">
                  <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <h4 class="font-semibold text-gray-800 mb-1">QR Oluşturulmadı</h4>
                  <p class="text-sm text-gray-500">QR oluşturmak için oturumu açmanız gerekir</p>
                </div>
              </div>
            </div>

            <!-- Attendance Card -->
            <div class="bg-gray-50 rounded-xl border border-gray-100 overflow-hidden">
              <div class="px-4 py-3 border-b border-gray-100 bg-white">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h3 class="font-semibold text-gray-800">Yoklama Kayıtları</h3>
                  </div>
                  <span class="badge badge-primary">{{ (session?.attendance || []).length }}</span>
                </div>
              </div>

              <div class="p-4 max-h-[450px] overflow-auto">
                <div v-if="(session?.attendance || []).length === 0" class="py-12 text-center">
                  <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <h4 class="font-semibold text-gray-800 mb-1">Henüz Yoklama Yok</h4>
                  <p class="text-sm text-gray-500">Öğrenciler QR tarayarak kayıt olduğunda burada görünür</p>
                </div>

                <div v-else class="space-y-2">
                  <div 
                    v-for="a in session?.attendance || []" 
                    :key="a.attendance_id"
                    class="bg-white rounded-xl p-4 border border-gray-100 hover:border-gray-200 hover:shadow-sm transition-all"
                  >
                    <div class="flex items-center justify-between gap-3">
                      <div class="flex items-center gap-3 min-w-0">
                        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center shrink-0">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                        </div>
                        <div class="min-w-0">
                          <div class="font-semibold text-gray-800 truncate">{{ a.student_name }}</div>
                          <div class="text-sm text-gray-500 truncate">{{ a.student_email }}</div>
                        </div>
                      </div>
                      <div class="text-right shrink-0">
                        <span class="badge badge-success badge-outline">{{ a.status }}</span>
                        <div class="text-xs text-gray-400 mt-1">{{ a.scanned_at || "-" }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { getApi } from "../lib/api";

const auth = useAuthStore();
const route = useRoute();

const sessionId = computed(() => String(route.params.id));
const loading = ref(false);
const errorMsg = ref<string | null>(null);

const session = ref<any | null>(null);
const qr = ref<any | null>(null);
const qrError = ref<string | null>(null);

async function fetchSession() {
  const api = await getApi();
  const resp = await api.get(`/api/instructor/sessions/${sessionId.value}`);
  session.value = resp.data.session;
}

async function refreshQr() {
  qrError.value = null;
  qr.value = null;
  try {
    const api = await getApi();
    const resp = await api.get(`/api/instructor/sessions/${sessionId.value}/qr`);
    qr.value = resp.data.qr;
  } catch (e: any) {
    qrError.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "QR alınamadı");
  }
}

async function toggleOpen(open: boolean) {
  loading.value = true;
  errorMsg.value = null;
  try {
    const api = await getApi();
    await api.post(`/api/instructor/sessions/${sessionId.value}/${open ? "open" : "close"}`);
    await refreshAll();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "İşlem başarısız");
  } finally {
    loading.value = false;
  }
}

async function refreshAll() {
  loading.value = true;
  errorMsg.value = null;
  try {
    await fetchSession();
    if (session.value?.is_open) await refreshQr();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Yüklenemedi");
  } finally {
    loading.value = false;
  }
}

onMounted(refreshAll);
watch(sessionId, refreshAll);
</script>
