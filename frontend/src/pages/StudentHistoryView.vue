<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-gradient-to-r from-amber-50 via-orange-50 to-transparent rounded-2xl p-6 border border-amber-100">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 bg-amber-100 rounded-2xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-800">Katılım Geçmişim</h1>
            <p class="text-gray-500 text-sm mt-1">Yoklama kayıtlarınızı görüntüleyin</p>
          </div>
        </div>
        <button 
          class="btn btn-primary gap-2 rounded-xl" 
          :disabled="loading" 
          @click="load"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" :class="{ 'animate-spin': loading }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ loading ? 'Yükleniyor...' : 'Yenile' }}
        </button>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="errorMsg" class="alert alert-warning rounded-xl">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-5 w-5" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span>{{ errorMsg }}</span>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-gradient-to-br from-primary/10 to-primary/5 rounded-2xl border border-primary/20 p-5 shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div>
            <div class="text-3xl font-bold text-primary">{{ items.length }}</div>
            <div class="text-sm text-gray-600 font-medium">Toplam Kayıt</div>
          </div>
        </div>
      </div>
      <div class="bg-gradient-to-br from-green-50 to-green-100/50 rounded-2xl border border-green-200 p-5 shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-green-200 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div class="text-3xl font-bold text-green-600">{{ presentCount }}</div>
            <div class="text-sm text-gray-600 font-medium">Katıldım</div>
          </div>
        </div>
      </div>
      <div class="bg-gradient-to-br from-amber-50 to-amber-100/50 rounded-2xl border border-amber-200 p-5 shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-amber-200 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div class="text-3xl font-bold text-amber-600">{{ lateCount }}</div>
            <div class="text-sm text-gray-600 font-medium">Geç Kaldım</div>
          </div>
        </div>
      </div>
      <div class="bg-gradient-to-br from-red-50 to-red-100/50 rounded-2xl border border-red-200 p-5 shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-red-200 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <div>
            <div class="text-3xl font-bold text-red-600">{{ absentCount }}</div>
            <div class="text-sm text-gray-600 font-medium">Katılmadım</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Table Card -->
    <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <!-- Table Header -->
      <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-transparent">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gray-100 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            <h2 class="font-bold text-gray-800">Yoklama Kayıtları</h2>
          </div>
          <span class="badge badge-primary">{{ items.length }} kayıt</span>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="table w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="font-semibold text-gray-600">ID</th>
              <th class="font-semibold text-gray-600">Oturum</th>
              <th class="font-semibold text-gray-600">Durum</th>
              <th class="font-semibold text-gray-600">Tarih/Saat</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="it in items" :key="it.id" class="hover:bg-gray-50 transition-colors">
              <td class="font-mono text-sm text-gray-600">#{{ it.id }}</td>
              <td class="font-mono text-sm text-gray-600">{{ it.session_id }}</td>
              <td>
                <span 
                  class="badge gap-1" 
                  :class="{
                    'badge-success text-white': it.status === 'PRESENT',
                    'badge-warning': it.status === 'LATE',
                    'badge-error text-white': it.status === 'ABSENT',
                    'badge-info': it.status === 'EXCUSED'
                  }"
                >
                  <svg v-if="it.status === 'PRESENT'" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <svg v-else-if="it.status === 'LATE'" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg v-else-if="it.status === 'ABSENT'" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  {{ statusText(it.status) }}
                </span>
              </td>
              <td class="text-sm text-gray-500">
                {{ formatDate(it.scanned_at) }}
              </td>
            </tr>
            <tr v-if="items.length === 0 && !loading">
              <td colspan="4" class="text-center py-12">
                <div class="flex flex-col items-center gap-3">
                  <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div class="text-gray-500">Henüz yoklama kaydınız bulunmuyor.</div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { getApi } from "../lib/api";

const items = ref<any[]>([]);
const loading = ref(false);
const errorMsg = ref<string | null>(null);

const presentCount = computed(() => items.value.filter(i => i.status === 'PRESENT').length);
const lateCount = computed(() => items.value.filter(i => i.status === 'LATE').length);
const absentCount = computed(() => items.value.filter(i => i.status === 'ABSENT').length);

function statusText(status: string) {
  const map: Record<string, string> = {
    'PRESENT': 'Katıldım',
    'LATE': 'Geç Kaldım',
    'ABSENT': 'Katılmadım',
    'EXCUSED': 'Mazeretli'
  };
  return map[status] || status;
}

function formatDate(dateStr: string | null) {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return date.toLocaleString('tr-TR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

async function load() {
  loading.value = true;
  errorMsg.value = null;
  try {
    const api = await getApi();
    const resp = await api.get("/api/student/attendance/history");
    items.value = resp.data.items;
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Yüklenemedi");
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>
