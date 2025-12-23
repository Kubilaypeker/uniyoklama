<template>
  <div class="space-y-4">
    <div v-if="auth.user?.role !== 'INSTRUCTOR'" class="alert alert-error">
      <span>Bu sayfa sadece INSTRUCTOR içindir.</span>
    </div>

    <div v-else class="space-y-4">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h1 class="text-2xl font-semibold">Derslerim</h1>
          <p class="text-sm opacity-80">
            Ders programını (meeting pattern) tanımla → sistem oturumları önceden oluştursun → derste tek tıkla QR aç.
          </p>
        </div>
        <button class="btn btn-sm" :disabled="loading" @click="load">
          <span v-if="loading" class="loading loading-spinner loading-sm"></span>
          Yenile
        </button>
      </div>

      <div v-if="errorMsg" class="alert alert-error">
        <span>{{ errorMsg }}</span>
      </div>

      <div v-if="items.length === 0 && !loading" class="alert">
        <span>Ders bulunamadı. (Demo için backend'de <code>flask seed</code> çalıştır.)</span>
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div v-for="o in items" :key="o.id" class="card bg-base-100 shadow-sm hover:shadow-md transition">
          <div class="card-body">
            <div class="flex items-start justify-between gap-3">
              <div>
                <h2 class="card-title">{{ o.course_code }} <span class="badge badge-outline">Şube {{ o.section }}</span></h2>
                <p class="text-sm opacity-80">{{ o.course_title }}</p>
                <p class="text-xs opacity-70">{{ o.term_code }}</p>
              </div>
              <div class="text-right text-xs opacity-70">
                <div>Oturum: <b>{{ o.sessions_total }}</b></div>
                <div>Program: <b>{{ o.meeting_patterns }}</b></div>
              </div>
            </div>

            <div class="divider my-2"></div>

            <div class="text-sm">
              <div class="opacity-80">Sonraki oturum</div>
              <div v-if="o.next_session_starts_at" class="font-medium">
                {{ formatDT(o.next_session_starts_at) }}
              </div>
              <div v-else class="opacity-60">Yok</div>
            </div>

            <div class="card-actions justify-end mt-2">
              <RouterLink class="btn btn-primary btn-sm" :to="{ name: 'instructorOffering', params: { id: o.id } }">
                Oturumlar & QR
              </RouterLink>
            </div>
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
