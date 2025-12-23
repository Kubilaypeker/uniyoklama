<template>
  <div class="space-y-4">
    <div class="card bg-base-100 shadow-sm">
      <div class="card-body">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="card-title">QR ile Yoklama</h2>
            <p class="text-sm opacity-80">
              Yoklamaya katılmak için <b>konum izni</b> ve <b>kamera izni</b> gerekir.
            </p>
          </div>

          <div class="badge badge-outline">
            {{ stepLabel }}
          </div>
        </div>

        <div v-if="errorMsg" class="alert alert-error mt-3">
          <span>{{ errorMsg }}</span>
        </div>
        <div v-if="successMsg" class="alert alert-success mt-3">
          <span>{{ successMsg }}</span>
        </div>

        <div v-if="token" class="alert mt-3">
          <span class="text-sm">
            QR okundu ✅ Token hazır. Şimdi konum izni verip yoklamaya katılabilirsin.
          </span>
        </div>

        <div class="mt-4 grid gap-4 md:grid-cols-2">
          <div class="card bg-base-200">
            <div class="card-body">
              <h3 class="font-semibold">Kamerayla QR Tara (opsiyonel)</h3>
              <p class="text-xs opacity-70">
                Eğer QR seni otomatik buraya getirmediyse (bazı cihazlarda), kamerayı açıp burada tarayabilirsin.
              </p>

              <div class="rounded-box overflow-hidden bg-black/80 aspect-video flex items-center justify-center">
                <video ref="videoRef" class="w-full h-full object-cover" playsinline muted></video>
              </div>

              <div class="flex flex-wrap gap-2">
                <button
                  class="btn btn-sm"
                  :class="scanning ? 'btn-warning' : 'btn-primary'"
                  :disabled="loading"
                  @click="scanning ? stopCamera() : startCamera()"
                >
                  <span v-if="scanning">Kamerayı Durdur</span>
                  <span v-else>Kamerayı Başlat</span>
                </button>

                <button class="btn btn-sm" :disabled="loading" @click="clearToken">
                  Tokeni Temizle
                </button>
              </div>
            </div>
          </div>

          <div class="card bg-base-200">
            <div class="card-body">
              <h3 class="font-semibold">Yoklamaya Katıl</h3>

              <label class="form-control w-full">
                <div class="label"><span class="label-text">Token</span></div>

                <input
                  :value="token"
                  @input="onTokenInput(($event.target as HTMLInputElement).value)"
                  class="input input-bordered w-full"
                  placeholder="QR ile gelen token otomatik dolacak"
                />

                <div class="label">
                  <span class="label-text-alt opacity-70">Token dolu değilse QR okut (üstte) veya QR linki ile gel.</span>
                </div>
              </label>

              <button class="btn btn-success" :disabled="loading || !token" @click="submitAttendance">
                <span v-if="loading" class="loading loading-spinner loading-sm"></span>
                Konumumu Al & Yoklamaya Katıl
              </button>

              <div class="text-xs opacity-70">
                Konum izni çıkmıyorsa: Tarayıcı ayarlarından “Location” izinlerini kontrol et.
              </div>
            </div>
          </div>
        </div>

        <div class="card bg-base-100 mt-4" v-if="debug">
          <div class="card-body">
            <h3 class="font-semibold">Debug</h3>
            <pre class="text-xs whitespace-pre-wrap">{{ debug }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRoute } from "vue-router";
import { BrowserQRCodeReader, type IScannerControls } from "@zxing/browser";
import { getApi } from "../lib/api";

const route = useRoute();
const token = ref("");
const loading = ref(false);
const scanning = ref(false);

const errorMsg = ref<string | null>(null);
const successMsg = ref<string | null>(null);
const debug = ref<string | null>(null);

const videoRef = ref<HTMLVideoElement | null>(null);

let reader: BrowserQRCodeReader | null = null;
let controls: IScannerControls | null = null;

const stepLabel = computed(() => {
  if (successMsg.value) return "✅ Tamam";
  if (loading.value) return "⏳ İşleniyor";
  if (token.value) return "📍 Konum İzni";
  if (scanning.value) return "📷 QR Tara";
  return "1) QR  2) Konum";
});

/**
 * ✅ QR içeriğinden token çıkarır:
 * - Eğer QR direkt token ise aynen döner
 * - Eğer QR tam URL ise (/scan?token=...), query paramdan token'ı alır
 */
function extractTokenFromQrText(text: string): string {
  const raw = (text || "").trim();
  if (!raw) return "";

  // Direkt token ise (URL değilse) kullan
  if (!raw.startsWith("http://") && !raw.startsWith("https://")) {
    return raw;
  }

  // URL ise token paramını ayıkla
  try {
    const u = new URL(raw);
    return (u.searchParams.get("token") || "").trim();
  } catch {
    return "";
  }
}

function onTokenInput(value: string) {
  const extracted = extractTokenFromQrText(value);
  // Eğer URL’den token çıkarabildiysek token'ı ona set et,
  // çıkaramadıysak kullanıcı yazıyor olabilir, ham hali bırak.
  token.value = extracted || value.trim();
}

onMounted(() => {
  // ✅ /scan?token=... ile gelirse otomatik token'a çevir
  const q = route.query.token;
  if (typeof q === "string" && q.trim()) {
    token.value = extractTokenFromQrText(q) || q.trim();
    if (token.value) {
      successMsg.value = "QR linki ile geldin ✅ Şimdi konum izni vererek yoklamaya katıl.";
    }
  }
});

onUnmounted(() => {
  stopCamera();
});

function clearToken() {
  token.value = "";
  successMsg.value = null;
  errorMsg.value = null;
  debug.value = null;
}

async function startCamera() {
  errorMsg.value = null;
  successMsg.value = null;
  debug.value = null;

  if (!videoRef.value) {
    errorMsg.value = "Video bileşeni bulunamadı.";
    return;
  }

  try {
    reader = new BrowserQRCodeReader();
    scanning.value = true;

    // Mobilde arka kamera için ideal
    const constraints: MediaStreamConstraints = {
      video: { facingMode: { ideal: "environment" } },
      audio: false,
    };

    controls = await reader.decodeFromConstraints(constraints, videoRef.value, (result) => {
      if (!result) return;

      const scannedText = result.getText();
      const extracted = extractTokenFromQrText(scannedText);

      if (!extracted) {
        errorMsg.value =
          "QR okundu ama token bulunamadı. QR'ın /scan?token=... içeren bir link olduğundan emin ol.";
        debug.value = `Scanned text:\n${scannedText}`;
        return;
      }

      token.value = extracted;
      successMsg.value = "QR okundu ✅ Şimdi konum izni vererek yoklamaya katıl.";
      debug.value = `Scanned text:\n${scannedText}\n\nExtracted token (first 16):\n${extracted.slice(0, 16)}...`;
      stopCamera();
    });
  } catch (e: any) {
    scanning.value = false;
    const msg = e?.message || "Kamera açılamadı. Tarayıcıdan kamera izni verildiğinden emin ol.";
    errorMsg.value = String(msg);
  }
}

function stopCamera() {
  try {
    controls?.stop();
  } catch (_) {}
  controls = null;
  scanning.value = false;
}

function getPosition(): Promise<GeolocationPosition> {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("Bu tarayıcı konum özelliğini desteklemiyor."));
      return;
    }
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      enableHighAccuracy: true,
      timeout: 15000,
      maximumAge: 0,
    });
  });
}

async function submitAttendance() {
  errorMsg.value = null;
  successMsg.value = null;
  debug.value = null;
  loading.value = true;

  try {
    token.value = extractTokenFromQrText(token.value) || token.value.trim();

    const pos = await getPosition();
    const lat = pos.coords.latitude;
    const lng = pos.coords.longitude;
    const accuracy_m = pos.coords.accuracy;

    const api = await getApi();
    console.log(token.value);
    const resp = await api.post("/api/student/attendance/scan", {
      token: token.value,
      lat,
      lng,
      accuracy_m,
    });

    successMsg.value = "Yoklama alındı ✅";
    debug.value = JSON.stringify(resp.data, null, 2);
  } catch (e: any) {
    const msg =
      e?.response?.data?.details ||
      e?.response?.data?.error ||
      e?.message ||
      "Yoklama alınamadı.";
    errorMsg.value = String(msg);
    if (e?.response?.data) debug.value = JSON.stringify(e.response.data, null, 2);
  } finally {
    loading.value = false;
  }
}
</script>
