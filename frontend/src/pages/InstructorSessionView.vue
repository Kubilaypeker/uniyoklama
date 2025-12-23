<template>
  <div class="space-y-4">
    <div v-if="auth.user?.role !== 'INSTRUCTOR'" class="alert alert-error">
      <span>Bu sayfa sadece INSTRUCTOR içindir.</span>
    </div>

    <div v-else class="space-y-4">
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h2 class="card-title">
                Session #{{ sessionId }}
                <span class="badge" :class="session?.is_open ? 'badge-success' : 'badge-ghost'">
                  {{ session?.is_open ? "Açık" : "Kapalı" }}
                </span>
              </h2>
              <p class="text-sm opacity-80">
                {{ session?.course_code }} - {{ session?.course_title }} ({{ session?.term_code }} / Şube {{ session?.section }})
              </p>
              <p class="text-xs opacity-70">
                {{ session?.starts_at }} → {{ session?.ends_at }}
              </p>
            </div>

            <div class="flex gap-2">
              <button class="btn btn-sm" :disabled="loading" @click="toggleOpen(true)">Aç</button>
              <button class="btn btn-sm" :disabled="loading" @click="toggleOpen(false)">Kapat</button>
              <button class="btn btn-sm btn-primary" :disabled="loading" @click="refreshAll">Yenile</button>
            </div>
          </div>

          <div class="divider"></div>

          <div class="grid gap-4 md:grid-cols-2">
            <div class="card bg-base-00">
              <div class="card-body">
                <h3 class="font-semibold">QR</h3>

                <div v-if="qrError" class="alert alert-warning">
                  <span>{{ qrError }}</span>
                </div>

                <div v-if="qr?.image_data_url" class="flex flex-col items-center gap-3">
                  <img :src="qr.image_data_url" alt="QR" class="max-w-[260px] rounded-box bg-white p-2" />
                  <div class="text-xs opacity-70 text-center">
                    QR süresi: {{ qr.expires_in }} sn<br />
                    Öğrenciler bu QR'ı okutarak <code>/scan</code> ekranına gider.
                  </div>
                  <button class="btn btn-sm" @click="refreshQr">QR Yenile</button>
                </div>

                <div v-else class="text-sm opacity-70">
                  QR oluşturmak için session açık olmalı.
                </div>
              </div>
            </div>

            <div class="card bg-base-200">
              <div class="card-body">
                <h3 class="font-semibold">Yoklama Kayıtları</h3>
                <div class="overflow-x-auto">
                  <table class="table table-sm">
                    <thead>
                      <tr>
                        <th>Öğrenci</th>
                        <th>Durum</th>
                        <th>Okutma</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="a in session?.attendance || []" :key="a.attendance_id">
                        <td>
                          <div class="font-medium">{{ a.student_name }}</div>
                          <div class="text-xs opacity-70">{{ a.student_email }}</div>
                        </td>
                        <td><span class="badge badge-outline">{{ a.status }}</span></td>
                        <td class="text-xs opacity-70">{{ a.scanned_at || "-" }}</td>
                      </tr>
                      <tr v-if="(session?.attendance || []).length === 0">
                        <td colspan="3" class="text-center text-sm opacity-70">Henüz yoklama yok.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>


        </div>
      </div>

      <div class="alert alert-warning" v-if="errorMsg">
        <span>{{ errorMsg }}</span>
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
