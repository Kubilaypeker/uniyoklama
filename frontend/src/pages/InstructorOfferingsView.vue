<template>
  <div class="space-y-6">
    <div v-if="auth.user?.role !== 'INSTRUCTOR'" class="alert alert-error rounded-xl shadow-sm">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>Bu sayfa sadece öğretim görevlileri içindir.</span>
    </div>

    <div v-else class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Derslerim</h1>
          <p class="text-gray-500 text-sm mt-1">
            Ders programını tanımla → sistem oturumları önceden oluştursun → derste tek tıkla QR aç.
          </p>
        </div>
        <button 
          class="btn btn-primary gap-2" 
          :disabled="loading" 
          @click="load"
        >
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Yenile
        </button>
      </div>

      <!-- Error Alert -->
      <div v-if="errorMsg" class="alert alert-error rounded-xl shadow-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ errorMsg }}</span>
      </div>

      <!-- Empty State -->
      <div v-if="items.length === 0 && !loading" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-12 text-center">
        <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Ders bulunamadı</h3>
        <p class="text-gray-500 text-sm">Henüz size atanmış ders bulunmamaktadır.</p>
        <p class="text-gray-400 text-xs mt-2">Demo için backend'de <code class="bg-gray-100 px-2 py-1 rounded">flask seed</code> çalıştırabilirsiniz.</p>
      </div>

      <!-- Course Cards Grid -->
      <div v-else class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        <div 
          v-for="o in items" 
          :key="o.id" 
          class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-lg hover:border-primary/20 transition-all duration-300 group"
        >
          <!-- Card Header -->
          <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-primary/5 to-transparent">
            <div class="flex items-start justify-between gap-3">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <h2 class="text-lg font-bold text-gray-800 truncate">{{ o.course_code }}</h2>
                  <span class="badge badge-primary badge-outline text-xs">Şube {{ o.section }}</span>
                </div>
                <p class="text-gray-600 text-sm mt-1 line-clamp-1">{{ o.course_title }}</p>
              </div>
              <div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center shrink-0 group-hover:bg-primary/20 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Card Body -->
          <div class="p-6 space-y-4">
            <!-- Term Badge -->
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{{ o.term_code }}</span>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-2 gap-3">
              <div class="bg-gray-50 rounded-xl p-3 text-center">
                <div class="text-2xl font-bold text-primary">{{ o.sessions_total }}</div>
                <div class="text-xs text-gray-500 mt-1">Oturum</div>
              </div>
              <div class="bg-gray-50 rounded-xl p-3 text-center">
                <div class="text-2xl font-bold text-green-600">{{ o.meeting_patterns }}</div>
                <div class="text-xs text-gray-500 mt-1">Haftalık</div>
              </div>
            </div>

            <!-- Next Session -->
            <div class="flex items-center gap-3 p-3 bg-blue-50 rounded-xl border border-blue-100">
              <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs text-blue-600 font-medium">Sonraki Oturum</div>
                <div v-if="o.next_session_starts_at" class="text-sm font-semibold text-gray-800 truncate">
                  {{ formatDT(o.next_session_starts_at) }}
                </div>
                <div v-else class="text-sm text-gray-400">Planlanmadı</div>
              </div>
            </div>

            <!-- Action Button -->
            <RouterLink 
              class="btn btn-primary w-full gap-2 h-12 rounded-xl text-sm font-semibold" 
              :to="{ name: 'instructorOffering', params: { id: o.id } }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
              </svg>
              Oturumlar & QR Yönetimi
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";
import { getApi } from "../lib/api";

const auth = useAuthStore();
const items = ref<any[]>([]);
const loading = ref(false);
const errorMsg = ref<string | null>(null);

function formatDT(iso: string) {
  // iso: YYYY-MM-DDTHH:MM:SS
  const [d, t] = iso.split("T");
  const [y, m, day] = d.split("-");
  const hhmm = (t || "").slice(0, 5);
  return `${day}.${m}.${y} ${hhmm}`;
}

async function load() {
  errorMsg.value = null;
  loading.value = true;
  try {
    const api = await getApi();
    const resp = await api.get("/api/instructor/offerings");
    items.value = resp.data.items || [];
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Yüklenemedi");
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>
