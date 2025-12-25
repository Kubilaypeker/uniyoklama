<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">QR ile Yoklama</h1>
        <p class="text-gray-500 text-sm mt-1">Yoklamaya katılmak için konum ve kamera izni gerekir</p>
      </div>
      <div 
        class="badge gap-2 px-4 py-3"
        :class="{
          'badge-success text-white': successMsg,
          'badge-warning': loading,
          'badge-info': token && !successMsg && !loading,
          'badge-ghost': !token && !successMsg && !loading
        }"
      >
        <svg v-if="successMsg" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <svg v-else-if="loading" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <svg v-else-if="token" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
        </svg>
        {{ stepLabel }}
      </div>
    </div>

    <!-- Success Alert -->
    <div v-if="successMsg" class="alert alert-success rounded-xl shadow-sm">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ successMsg }}</span>
    </div>

    <!-- Error Alert -->
    <div v-if="errorMsg" class="alert alert-error rounded-xl shadow-sm">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ errorMsg }}</span>
    </div>

    <!-- Token Ready Alert -->
    <div v-if="token && !successMsg && !errorMsg" class="alert bg-blue-50 border border-blue-200 rounded-xl">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span class="text-blue-800">QR okundu ✅ Token hazır. Şimdi konum izni verip yoklamaya katılabilirsiniz.</span>
    </div>

    <!-- Main Cards -->
    <div class="grid gap-6 lg:grid-cols-2">
      <!-- QR Scanner Card -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">Kamerayla QR Tara</h3>
              <p class="text-xs text-gray-500">QR linki ile gelmediyseniz burada tarayabilirsiniz</p>
            </div>
          </div>
        </div>
        
        <div class="p-6 space-y-4">
          <!-- Video Container -->
          <div class="relative rounded-xl overflow-hidden bg-gray-900 aspect-video flex items-center justify-center">
            <video ref="videoRef" class="w-full h-full object-cover" playsinline muted></video>
            
            <!-- Scanner Overlay -->
            <div v-if="!scanning" class="absolute inset-0 flex flex-col items-center justify-center bg-gray-900/80 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-500 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
              </svg>
              <p class="text-gray-400 text-sm">Kamerayı başlatmak için aşağıdaki butona tıklayın</p>
            </div>

            <!-- Scanning Indicator -->
            <div v-if="scanning" class="absolute inset-0 pointer-events-none">
              <div class="absolute inset-4 border-2 border-primary/50 rounded-lg"></div>
              <div class="absolute top-1/2 left-4 right-4 h-0.5 bg-primary/70 animate-pulse"></div>
            </div>
          </div>

          <!-- Camera Controls -->
          <div class="flex flex-wrap gap-3">
            <button
              class="btn flex-1 gap-2"
              :class="scanning ? 'btn-warning' : 'btn-primary'"
              :disabled="loading"
              @click="scanning ? stopCamera() : startCamera()"
            >
              <svg v-if="!scanning" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
              </svg>
              {{ scanning ? 'Kamerayı Durdur' : 'Kamerayı Başlat' }}
            </button>

            <button 
              class="btn btn-ghost gap-2" 
              :disabled="loading || !token" 
              @click="clearToken"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Temizle
            </button>
          </div>
        </div>
      </div>

      <!-- Attendance Submit Card -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">Yoklamaya Katıl</h3>
              <p class="text-xs text-gray-500">Konum izni vererek yoklamanızı tamamlayın</p>
            </div>
          </div>
        </div>

        <div class="p-6 space-y-5">
          <!-- Token Input -->
          <div class="form-control">
            <label class="label pb-1">
              <span class="label-text font-medium text-gray-700">Yoklama Token</span>
              <span v-if="token" class="label-text-alt text-green-600 flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Hazır
              </span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
              </div>
              <input
                :value="token"
                @input="onTokenInput(($event.target as HTMLInputElement).value)"
                class="input input-bordered w-full pl-12 h-12 rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20"
                :class="{ 'border-green-500 bg-green-50/30': token }"
                placeholder="QR ile gelen token otomatik dolacak"
              />
            </div>
            <label class="label pt-1">
              <span class="label-text-alt text-gray-400">Token yoksa QR okutun veya QR linki ile gelin</span>
            </label>
          </div>

          <!-- Submit Button -->
          <button 
            class="btn btn-success w-full h-14 rounded-xl text-base gap-2" 
            :disabled="loading || !token" 
            @click="submitAttendance"
          >
            <span v-if="loading" class="loading loading-spinner"></span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {{ loading ? 'Konum alınıyor...' : 'Konumumu Al ve Yoklamaya Katıl' }}
          </button>

          <!-- Help Text -->
          <div class="flex items-start gap-3 p-4 bg-amber-50 rounded-xl border border-amber-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="text-sm text-amber-800">
              <p class="font-medium">Konum izni gereklidir</p>
              <p class="text-amber-700 mt-1">Konum izni çıkmıyorsa tarayıcı ayarlarından "Location" izinlerini kontrol edin.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Debug Card (Hidden by default) -->
    <div v-if="debug" class="bg-gray-50 rounded-2xl border border-gray-200 overflow-hidden">
      <div class="px-6 py-3 bg-gray-100 border-b border-gray-200">
        <h3 class="font-mono text-sm text-gray-600">Debug Bilgisi</h3>
      </div>
      <div class="p-6">
        <pre class="text-xs text-gray-600 whitespace-pre-wrap font-mono bg-white p-4 rounded-lg border">{{ debug }}</pre>
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
  if (successMsg.value) return "Tamamlandı";
  if (loading.value) return "İşleniyor...";
  if (token.value) return "Konum İzni Ver";
  if (scanning.value) return "QR Taranıyor";
  return "QR Bekliyor";
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
  // Eğer URL'den token çıkarabildiysek token'ı ona set et,
  // çıkaramadıysak kullanıcı yazıyor olabilir, ham hali bırak.
  token.value = extracted || value.trim();
}

onMounted(() => {
  // ✅ /scan?token=... ile gelirse otomatik token'a çevir
  const q = route.query.token;
  if (typeof q === "string" && q.trim()) {
    token.value = extractTokenFromQrText(q) || q.trim();
    if (token.value) {
      successMsg.value = "QR linki ile geldiniz ✅ Şimdi konum izni vererek yoklamaya katılın.";
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
          "QR okundu ama token bulunamadı. QR'ın /scan?token=... içeren bir link olduğundan emin olun.";
        debug.value = `Scanned text:\n${scannedText}`;
        return;
      }

      token.value = extracted;
      successMsg.value = "QR okundu ✅ Şimdi konum izni vererek yoklamaya katılın.";
      debug.value = `Scanned text:\n${scannedText}\n\nExtracted token (first 16):\n${extracted.slice(0, 16)}...`;
      stopCamera();
    });
  } catch (e: any) {
    scanning.value = false;
    const msg = e?.message || "Kamera açılamadı. Tarayıcıdan kamera izni verildiğinden emin olun.";
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

    successMsg.value = "Yoklama başarıyla alındı ✅";
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
