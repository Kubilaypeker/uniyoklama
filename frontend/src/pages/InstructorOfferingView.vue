<template>
  <div class="space-y-8">
    <div v-if="auth.user?.role !== 'INSTRUCTOR'" class="alert alert-error">
      <span>Bu sayfa sadece INSTRUCTOR içindir.</span>
    </div>

    <div v-else class="space-y-4">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h1 class="text-2xl font-semibold">{{ offeringTitle }}</h1>
          <p class="text-sm opacity-80">
            Oturumlar önceden oluşturulur. Derste sadece ilgili oturumu <b>Aç</b> → QR göster → öğrenciler konum
            doğrulamayla yoklamaya girer.
          </p>
        </div>

        <div class="flex gap-2">
          <RouterLink class="btn btn-sm" to="/instructor">← Derslerim</RouterLink>
          <button class="btn btn-sm btn-primary" :disabled="loading" @click="refreshAll">
            <span v-if="loading" class="loading loading-spinner loading-sm"></span>
            Yenile
          </button>
        </div>
      </div>

      <div v-if="errorMsg" class="alert alert-error">
        <span>{{ errorMsg }}</span>
      </div>

      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h2 class="card-title">Ders Programı (Meeting Pattern)</h2>
              <p class="text-xs opacity-70">
                Buradan haftalık ders gün/saatini ekleyebilirsin. Ekledikten sonra oturumlar otomatik üretilir.
              </p>
            </div>
            <button class="btn btn-sm" :disabled="loading" @click="generateSessions">
              Oturumları Oluştur
            </button>
          </div>

          <div class="grid gap-3 md:grid-cols-4 mt-3">
            <label class="form-control">
              <div class="label"><span class="label-text">Gün</span></div>
              <select class="select select-bordered" v-model.number="mpWeekday">
                <option :value="0">Pazartesi</option>
                <option :value="1">Salı</option>
                <option :value="2">Çarşamba</option>
                <option :value="3">Perşembe</option>
                <option :value="4">Cuma</option>
                <option :value="5">Cumartesi</option>
                <option :value="6">Pazar</option>
              </select>
            </label>

            <label class="form-control">
              <div class="label"><span class="label-text">Başlangıç</span></div>
              <input class="input input-bordered" type="time" v-model="mpStart" />
            </label>

            <label class="form-control">
              <div class="label"><span class="label-text">Bitiş</span></div>
              <input class="input input-bordered" type="time" v-model="mpEnd" />
            </label>

            <div class="flex items-end">
              <button class="btn btn-success w-full" :disabled="loading" @click="addMeetingPattern">
                Program Ekle
              </button>
            </div>
          </div>

          <div class="divider my-3"></div>

          <div class="overflow-x-auto">
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>Gün</th>
                  <th>Saat</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in meetingPatterns" :key="p.id">
                  <td>{{ weekdayLabel(p.weekday) }}</td>
                  <td>{{ p.starts_time }} - {{ p.ends_time }}</td>
                  <td class="text-right">
                    <button class="btn btn-ghost btn-xs" :disabled="loading" @click="deleteMeetingPattern(p.id)">Sil</button>
                  </td>
                </tr>
                <tr v-if="meetingPatterns.length === 0">
                  <td colspan="3" class="text-center text-sm opacity-70">Henüz program eklenmedi.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="grid gap-4 lg:grid-cols-3">
        <div class="card bg-base-100 shadow-sm lg:col-span-1">
          <div class="card-body">
            <h2 class="card-title">Oturumlar</h2>
            <p class="text-xs opacity-70">Bugünü bulup seçmek için listeyi kullan.</p>

            <div class="divider my-2"></div>

            <div class="space-y-2 max-h-[520px] overflow-auto pr-1">
              <button
                v-for="s in sessions"
                :key="s.id"
                class="btn btn-sm w-full justify-between"
                :class="selectedSessionId === s.id ? 'btn-primary' : 'btn-ghost'"
                @click="selectSession(s.id)"
              >
                <span class="text-left">
                  <div class="font-medium">{{ formatDT(s.starts_at) }}</div>
                  <div class="text-xs opacity-70">Kayıt: {{ s.attendance_count }}</div>
                </span>
                <span class="badge" :class="s.is_open ? 'badge-success' : 'badge-ghost'" style="font-size: 8px">
                  {{ s.is_open ? "Açık" : "Kapalı" }}
                </span>
              </button>

              <div v-if="sessions.length === 0 && !loading" class="text-sm opacity-70">
                Oturum yok. Program ekleyip “Oturumları Oluştur” yap.
              </div>
            </div>
          </div>
        </div>

        <div class="card bg-base-100 shadow-sm lg:col-span-2">
          <div class="card-body">
            <div v-if="!selectedSessionId" class="text-sm opacity-70">
              Soldan bir oturum seç.
            </div>

            <div v-else>
              <div class="flex items-start justify-between gap-4">
                <div>
                  <h2 class="card-title">
                    Oturum #{{ selectedSessionId }}
                    <span class="badge" :class="sessionDetail?.is_open ? 'badge-success' : 'badge-ghost'">
                      {{ sessionDetail?.is_open ? "Açık" : "Kapalı" }}
                    </span>
                  </h2>
                  <p class="text-xs opacity-70">
                    {{ sessionDetail?.starts_at }} → {{ sessionDetail?.ends_at }}
                  </p>
                </div>

                <div class="flex flex-wrap gap-2">
                  <button class="btn btn-sm" :disabled="loading" @click="toggleOpen(true)">Aç</button>
                  <button class="btn btn-sm" :disabled="loading" @click="toggleOpen(false)">Kapat</button>
                  <button class="btn btn-sm btn-primary" :disabled="loading" @click="refreshSelectedSession">Yenile</button>
                </div>
              </div>

              <div class="divider my-3"></div>

              <div class="grid gap-4 md:grid-cols-2">
                <div class="card bg-base-100">
                  <div class="card-body">
                    <h3 class="font-semibold">QR</h3>

                    <div v-if="qrError" class="alert alert-warning">
                      <span>{{ qrError }}</span>
                    </div>

                    <div v-if="qr?.image_data_url" class="flex flex-col items-center gap-3">
                      <img :src="qr.image_data_url" alt="QR" class="max-w-[320px] rounded-box bg-white p-2" />

                      <div class="text-xs opacity-70 text-center">
                        QR süresi:
                        <b>{{ qrSecondsLeft ?? qr.expires_in }}</b> sn<br />
                        Öğrenciler telefon kamerasıyla okutunca otomatik <code>/scan</code> ekranına gelir.<br />
                        <span class="opacity-70">Otomatik yenileme aktif ✅</span>
                      </div>

                      <button class="btn btn-sm" :disabled="loading" @click="refreshQr">QR Yenile</button>
                    </div>

                    <div v-else class="text-sm opacity-70">
                      QR göstermek için oturum açık olmalı.
                    </div>
                  </div>
                </div>

                <div class="card bg-base-100">
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
                          <tr v-for="a in sessionDetail?.attendance || []" :key="a.attendance_id">
                            <td>
                              <div class="font-medium">{{ a.student_name }}</div>
                              <div class="text-xs opacity-70">{{ a.student_email }}</div>
                            </td>
                            <td><span class="badge badge-outline">{{ a.status }}</span></td>
                            <td class="text-xs opacity-70">{{ a.scanned_at || "-" }}</td>
                          </tr>
                          <tr v-if="(sessionDetail?.attendance || []).length === 0">
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { getApi } from "../lib/api";

const auth = useAuthStore();
const route = useRoute();

const offeringId = computed(() => String(route.params.id));
const loading = ref(false);
const errorMsg = ref<string | null>(null);

const offeringTitle = ref("Ders");

const meetingPatterns = ref<any[]>([]);
const sessions = ref<any[]>([]);

const selectedSessionId = ref<number | null>(null);
const sessionDetail = ref<any | null>(null);
const qr = ref<any | null>(null);
const qrError = ref<string | null>(null);

// ✅ QR auto-refresh timer
const qrSecondsLeft = ref<number | null>(null);
let qrTimer: number | null = null;

function stopQrTimer() {
  if (qrTimer) {
    clearInterval(qrTimer);
    qrTimer = null;
  }
  qrSecondsLeft.value = null;
}

function startQrTimer(ttlSeconds: number) {
  stopQrTimer();
  qrSecondsLeft.value = ttlSeconds;

  qrTimer = window.setInterval(async () => {
    if (qrSecondsLeft.value == null) return;

    qrSecondsLeft.value -= 1;

    // Oturum kapanmışsa timer'ı durdur
    if (!sessionDetail.value?.is_open) {
      stopQrTimer();
      return;
    }

    if (qrSecondsLeft.value <= 0) {
      // Süre doldu -> yeni QR al
      await refreshQr();
    }
  }, 1000);
}

// Meeting pattern form
const mpWeekday = ref<number>(0);
const mpStart = ref<string>("10:00");
const mpEnd = ref<string>("11:00");

function weekdayLabel(w: number) {
  return ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][w] || String(w);
}

function formatDT(iso: string) {
  const [d, t] = iso.split("T");
  const [y, m, day] = d.split("-");
  const hhmm = (t || "").slice(0, 5);
  return `${day}.${m}.${y} ${hhmm}`;
}

function todayStrLocal() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, "0");
  const d = String(now.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

async function loadOfferingTitle() {
  // Basit: offerings listesinden başlığı bul
  const api = await getApi();
  const resp = await api.get("/api/instructor/offerings");
  const item = (resp.data.items || []).find((x: any) => String(x.id) === offeringId.value);
  if (item) offeringTitle.value = `${item.course_code} - ${item.course_title} (Şube ${item.section})`;
}

async function loadMeetingPatterns() {
  const api = await getApi();
  const resp = await api.get(`/api/instructor/offerings/${offeringId.value}/meeting-patterns`);
  meetingPatterns.value = resp.data.items || [];
}

async function loadSessions() {
  const api = await getApi();
  const resp = await api.get(`/api/instructor/offerings/${offeringId.value}/sessions`);
  sessions.value = resp.data.items || [];

  // İlk açılışta: bugünkü oturumu seçmeye çalış
  if (!selectedSessionId.value && sessions.value.length > 0) {
    const today = todayStrLocal();
    const todaySession = sessions.value.find((s: any) => String(s.starts_at).slice(0, 10) === today);
    const pick =
      todaySession ||
      sessions.value.find((s: any) => new Date(String(s.starts_at)).getTime() >= Date.now()) ||
      sessions.value[0];

    if (pick) {
      selectedSessionId.value = pick.id;
      await refreshSelectedSession();
    }
  }
}

async function refreshSelectedSession() {
  if (!selectedSessionId.value) return;

  qr.value = null;
  qrError.value = null;
  stopQrTimer(); // ✅ session değiştiyse eski timer'ı kapat

  const api = await getApi();
  const resp = await api.get(`/api/instructor/sessions/${selectedSessionId.value}`);
  sessionDetail.value = resp.data.session;

  if (sessionDetail.value?.is_open) {
    await refreshQr();
  } else {
    stopQrTimer();
  }
}

async function refreshQr() {
  if (!selectedSessionId.value) return;

  qrError.value = null;
  qr.value = null;

  try {
    const api = await getApi();
    const resp = await api.get(`/api/instructor/sessions/${selectedSessionId.value}/qr`);
    qr.value = resp.data.qr;

    // ✅ yeni QR geldi -> TTL'e göre otomatik geri sayım başlat
    const ttl = Number(qr.value?.expires_in ?? 120);
    startQrTimer(Math.max(5, ttl));
  } catch (e: any) {
    stopQrTimer();
    qrError.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "QR alınamadı");
  }
}

async function toggleOpen(open: boolean) {
  if (!selectedSessionId.value) return;
  loading.value = true;
  errorMsg.value = null;

  try {
    const api = await getApi();
    await api.post(`/api/instructor/sessions/${selectedSessionId.value}/${open ? "open" : "close"}`);
    await refreshAll();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "İşlem başarısız");
  } finally {
    loading.value = false;
  }
}

async function selectSession(id: number) {
  selectedSessionId.value = id;
  await refreshSelectedSession();
}

async function addMeetingPattern() {
  loading.value = true;
  errorMsg.value = null;
  try {
    const api = await getApi();
    await api.post(`/api/instructor/offerings/${offeringId.value}/meeting-patterns`, {
      weekday: mpWeekday.value,
      starts_time: mpStart.value,
      ends_time: mpEnd.value,
    });
    await refreshAll();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Eklenemedi");
  } finally {
    loading.value = false;
  }
}

async function deleteMeetingPattern(id: number) {
  loading.value = true;
  errorMsg.value = null;
  try {
    const api = await getApi();
    await api.delete(`/api/instructor/meeting-patterns/${id}`);
    await refreshAll();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Silinemedi");
  } finally {
    loading.value = false;
  }
}

async function generateSessions() {
  loading.value = true;
  errorMsg.value = null;
  try {
    const api = await getApi();
    await api.post(`/api/instructor/offerings/${offeringId.value}/generate-sessions`);
    await refreshAll();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Üretilemedi");
  } finally {
    loading.value = false;
  }
}

async function refreshAll() {
  loading.value = true;
  errorMsg.value = null;
  try {
    await loadOfferingTitle();
    await loadMeetingPatterns();
    await loadSessions();
    if (selectedSessionId.value) await refreshSelectedSession();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Yüklenemedi");
  } finally {
    loading.value = false;
  }
}

onMounted(refreshAll);

watch(offeringId, () => {
  selectedSessionId.value = null;
  sessionDetail.value = null;
  stopQrTimer();
  refreshAll();
});

// ✅ Sayfadan çıkarken interval leak olmasın
onUnmounted(() => stopQrTimer());
</script>
