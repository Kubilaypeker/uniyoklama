<template>
  <div class="space-y-4">
    <div class="hero bg-base-100 rounded-box shadow-sm">
      <div class="hero-content flex-col items-start">
        <h1 class="text-2xl font-semibold">UniYoklama</h1>
      </div>
    </div>

    <div v-if="auth.user?.role === 'INSTRUCTOR'" class="grid gap-4 md:grid-cols-2">
      <RouterLink class="card bg-base-100 shadow-sm hover:shadow-md transition" to="/instructor">
        <div class="card-body">
          <h2 class="card-title">Derslerim & Oturumlar</h2>
          <p class="text-sm opacity-80">
            Ders programını (meeting pattern) ekle, oturumları otomatik oluştur, derste tek tıkla QR aç.
          </p>
        </div>
      </RouterLink>

      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <h2 class="card-title">Derste Akış</h2>
          <ol class="text-sm opacity-80 list-decimal ml-5 space-y-1">
            <li>Bugünkü oturumu seç</li>
            <li>Oturumu <b>Aç</b></li>
            <li>QR'ı yansıt</li>
            <li>Öğrenciler telefon kamerasıyla okutunca otomatik <code>/scan</code> açılır</li>
          </ol>
        </div>
      </div>
    </div>

    <div v-else-if="auth.user?.role === 'STUDENT'" class="grid gap-4 md:grid-cols-2">
      <RouterLink class="card bg-base-100 shadow-sm hover:shadow-md transition" to="/scan">
        <div class="card-body">
          <h2 class="card-title">QR ile Yoklama</h2>
          <p class="text-sm opacity-80">
            QR linkiyle geldiysen token otomatik dolacak. Konum izni verip yoklamaya katıl.
          </p>
        </div>
      </RouterLink>

      <RouterLink class="card bg-base-100 shadow-sm hover:shadow-md transition" to="/student/history">
        <div class="card-body">
          <h2 class="card-title">Katılım Geçmişim</h2>
          <p class="text-sm opacity-80">Son 100 yoklama kaydını gösterir.</p>
        </div>
      </RouterLink>
    </div>

    <div v-else class="alert">
      <span>Kullanıcı rolüne göre ekranlar genişletilebilir (STAFF/ADMIN).</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "../stores/auth";
const auth = useAuthStore();
</script>
