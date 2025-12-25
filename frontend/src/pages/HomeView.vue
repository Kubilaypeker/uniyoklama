<template>
  <div class="space-y-6">
    <!-- Welcome Header -->
    <div class="bg-gradient-to-r from-primary/10 via-primary/5 to-transparent rounded-2xl p-6 md:p-8">
      <div class="flex items-center gap-4">
        <div class="w-14 h-14 bg-primary/20 rounded-2xl flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
          </svg>
        </div>
        <div>
          <h1 class="text-2xl md:text-3xl font-bold text-gray-800">
            Hoş Geldiniz, {{ auth.user?.full_name || 'Öğrenci' }}!
          </h1>
          <p class="text-gray-500 mt-1">Selçuk Üniversitesi Online Yoklama Sistemi</p>
        </div>
      </div>
    </div>

    <!-- Instructor View -->
    <div v-if="auth.user?.role === 'INSTRUCTOR'" class="grid gap-5 md:grid-cols-2">
      <RouterLink 
        class="group card bg-white border border-gray-100 shadow-sm hover:shadow-lg hover:border-primary/30 transition-all duration-300 rounded-2xl overflow-hidden" 
        to="/instructor"
      >
        <div class="card-body p-6">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <div class="flex-1">
              <h2 class="text-lg font-semibold text-gray-800 group-hover:text-primary transition-colors">
                Derslerim & Oturumlar
              </h2>
              <p class="text-sm text-gray-500 mt-1">
                Ders programını ekle, oturumları oluştur ve derste tek tıkla QR aç.
              </p>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-300 group-hover:text-primary group-hover:translate-x-1 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </RouterLink>

      <div class="card bg-white border border-gray-100 shadow-sm rounded-2xl">
        <div class="card-body p-6">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            <div class="flex-1">
              <h2 class="text-lg font-semibold text-gray-800">Derste Akış</h2>
              <ol class="text-sm text-gray-500 mt-3 space-y-2">
                <li class="flex items-center gap-2">
                  <span class="w-5 h-5 bg-primary/10 text-primary rounded-full text-xs flex items-center justify-center font-medium">1</span>
                  Bugünkü oturumu seç
                </li>
                <li class="flex items-center gap-2">
                  <span class="w-5 h-5 bg-primary/10 text-primary rounded-full text-xs flex items-center justify-center font-medium">2</span>
                  Oturumu <span class="font-medium text-gray-700">Aç</span>
                </li>
                <li class="flex items-center gap-2">
                  <span class="w-5 h-5 bg-primary/10 text-primary rounded-full text-xs flex items-center justify-center font-medium">3</span>
                  QR'ı yansıt
                </li>
                <li class="flex items-center gap-2">
                  <span class="w-5 h-5 bg-primary/10 text-primary rounded-full text-xs flex items-center justify-center font-medium">4</span>
                  Öğrenciler tarar, otomatik katılır
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Student View -->
    <div v-else-if="auth.user?.role === 'STUDENT'" class="grid gap-5 md:grid-cols-2">
      <!-- QR Scan Card -->
      <RouterLink 
        class="group card bg-gradient-to-br from-primary to-primary/80 shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-300 rounded-2xl overflow-hidden text-white" 
        to="/scan"
      >
        <div class="card-body p-6">
          <div class="flex items-start gap-4">
            <div class="w-14 h-14 bg-white/20 backdrop-blur rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
              </svg>
            </div>
            <div class="flex-1">
              <h2 class="text-xl font-bold">
                QR ile Yoklama
              </h2>
              <p class="text-white/80 text-sm mt-2">
                Kameranızla QR kodu tarayın veya linke tıklayarak yoklamaya katılın.
              </p>
              <div class="mt-4 flex items-center gap-2 text-sm font-medium">
                <span>Şimdi Tara</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </RouterLink>

      <!-- History Card -->
      <RouterLink 
        class="group card bg-white border border-gray-100 shadow-sm hover:shadow-lg hover:border-primary/30 transition-all duration-300 rounded-2xl overflow-hidden" 
        to="/student/history"
      >
        <div class="card-body p-6">
          <div class="flex items-start gap-4">
            <div class="w-14 h-14 bg-amber-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="flex-1">
              <h2 class="text-xl font-semibold text-gray-800 group-hover:text-primary transition-colors">
                Katılım Geçmişim
              </h2>
              <p class="text-gray-500 text-sm mt-2">
                Tüm yoklama kayıtlarınızı görüntüleyin ve takip edin.
              </p>
              <div class="mt-4 flex items-center gap-2 text-sm font-medium text-primary">
                <span>Geçmişi Görüntüle</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </RouterLink>
    </div>

    <!-- Other Roles -->
    <div v-else class="alert bg-blue-50 border border-blue-200 rounded-2xl">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span class="text-blue-800">Kullanıcı rolüne göre ekranlar genişletilebilir (STAFF/ADMIN).</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "../stores/auth";
const auth = useAuthStore();
</script>
