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
          <h1 class="text-2xl font-bold text-gray-800">{{ offeringTitle }}</h1>
          <p class="text-gray-500 text-sm mt-1">
            Oturumlar önceden oluşturulur. Derste sadece ilgili oturumu <b>Aç</b> → QR göster → öğrenciler konum
            doğrulamayla yoklamaya girer.
          </p>
        </div>

        <div class="flex gap-2">
          <RouterLink class="btn btn-ghost gap-2" to="/instructor">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Derslerim
          </RouterLink>
          <button class="btn btn-primary gap-2" :disabled="loading" @click="refreshAll">
            <span v-if="loading" class="loading loading-spinner loading-sm"></span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Yenile
          </button>
        </div>
      </div>

      <!-- Error Alert -->
      <div v-if="errorMsg" class="alert alert-error rounded-xl shadow-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ errorMsg }}</span>
      </div>

      <!-- Meeting Pattern Card -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-purple-50 to-transparent">
          <div class="flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h2 class="text-lg font-bold text-gray-800">Ders Programı</h2>
                <p class="text-xs text-gray-500">Haftalık ders gün/saatini ekleyebilirsin. Ekledikten sonra oturumlar otomatik üretilir.</p>
              </div>
            </div>
            <button 
              class="btn btn-primary btn-sm gap-2" 
              :disabled="loading" 
              @click="generateSessions"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              Oturumları Oluştur
            </button>
          </div>
        </div>

        <div class="p-6">
          <!-- Add Pattern Form -->
          <div class="grid gap-4 md:grid-cols-4">
            <div class="form-control">
              <label class="label pb-1">
                <span class="label-text font-medium text-gray-700">Gün</span>
              </label>
              <select class="select select-bordered w-full h-12 rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20" v-model.number="mpWeekday">
                <option :value="0">Pazartesi</option>
                <option :value="1">Salı</option>
                <option :value="2">Çarşamba</option>
                <option :value="3">Perşembe</option>
                <option :value="4">Cuma</option>
                <option :value="5">Cumartesi</option>
                <option :value="6">Pazar</option>
              </select>
            </div>

            <div class="form-control">
              <label class="label pb-1">
                <span class="label-text font-medium text-gray-700">Başlangıç</span>
              </label>
              <input class="input input-bordered w-full h-12 rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20" type="time" v-model="mpStart" />
            </div>

            <div class="form-control">
              <label class="label pb-1">
                <span class="label-text font-medium text-gray-700">Bitiş</span>
              </label>
              <input class="input input-bordered w-full h-12 rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20" type="time" v-model="mpEnd" />
            </div>

            <div class="flex items-end">
              <button class="btn btn-success w-full h-12 rounded-xl gap-2" :disabled="loading" @click="addMeetingPattern">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Program Ekle
              </button>
            </div>
          </div>

          <!-- Meeting Pattern Table -->
          <div class="mt-6 overflow-x-auto">
            <table class="table w-full">
              <thead>
                <tr class="bg-gray-50">
                  <th class="rounded-tl-lg">Gün</th>
                  <th>Saat Aralığı</th>
                  <th class="text-right rounded-tr-lg">İşlem</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in meetingPatterns" :key="p.id" class="hover:bg-gray-50 transition-colors">
                  <td>
                    <div class="flex items-center gap-2">
                      <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                        <span class="text-xs font-bold text-purple-600">{{ weekdayLabel(p.weekday).slice(0, 2) }}</span>
                      </div>
                      <span class="font-medium">{{ weekdayLabel(p.weekday) }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="badge badge-ghost gap-1 px-3 py-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {{ p.starts_time }} - {{ p.ends_time }}
                    </span>
                  </td>
                  <td class="text-right">
                    <button class="btn btn-ghost btn-sm text-error hover:bg-error/10" :disabled="loading" @click="deleteMeetingPattern(p.id)">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Sil
                    </button>
                  </td>
                </tr>
                <tr v-if="meetingPatterns.length === 0">
                  <td colspan="3" class="text-center py-8">
                    <div class="flex flex-col items-center gap-2 text-gray-400">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="text-sm">Henüz program eklenmedi</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Announcement Card -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-amber-50 to-transparent">
          <div class="flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
                </svg>
              </div>
              <div>
                <h2 class="text-lg font-bold text-gray-800">Duyurular</h2>
                <p class="text-xs text-gray-500">Dersi alan öğrencilere duyuru yapabilirsiniz</p>
              </div>
            </div>
            <span class="badge badge-warning badge-outline">{{ announcements.length }} duyuru</span>
          </div>
        </div>

        <div class="p-6">
          <!-- Add Announcement Form -->
          <div class="grid gap-4 md:grid-cols-3">
            <div class="form-control">
              <label class="label pb-1">
                <span class="label-text font-medium text-gray-700">Başlık</span>
              </label>
              <input 
                class="input input-bordered w-full h-12 rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20" 
                type="text" 
                v-model="annTitle" 
                placeholder="Örn: Ders iptali" 
              />
            </div>

            <div class="form-control">
              <label class="label pb-1">
                <span class="label-text font-medium text-gray-700">Açıklama (opsiyonel)</span>
              </label>
              <input 
                class="input input-bordered w-full h-12 rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20" 
                type="text" 
                v-model="annContent" 
                placeholder="Duyuru detayı..." 
              />
            </div>

            <div class="flex items-end">
              <button class="btn btn-warning w-full h-12 rounded-xl gap-2" :disabled="loading || !annTitle.trim()" @click="addAnnouncement">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Duyuru Ekle
              </button>
            </div>
          </div>

          <!-- Announcements List -->
          <div v-if="announcements.length > 0" class="mt-6 space-y-3">
            <div 
              v-for="ann in announcements" 
              :key="ann.id"
              class="bg-amber-50 rounded-xl p-4 border border-amber-100"
            >
              <div class="flex items-start justify-between gap-3">
                <div class="flex-1 min-w-0">
                  <h4 class="font-semibold text-gray-800">{{ ann.title }}</h4>
                  <p v-if="ann.content" class="text-sm text-gray-600 mt-1">{{ ann.content }}</p>
                  <p class="text-xs text-gray-400 mt-2">{{ formatDT(ann.created_at) }}</p>
                </div>
                <button 
                  class="btn btn-ghost btn-sm text-error hover:bg-error/10" 
                  :disabled="loading" 
                  @click="deleteAnnouncement(ann.id)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="mt-6 text-center py-6">
            <div class="flex flex-col items-center gap-2 text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
              </svg>
              <span class="text-sm">Henüz duyuru yok</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sessions Grid -->
      <div class="grid gap-6 lg:grid-cols-3">
        <!-- Sessions List Card -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden lg:col-span-1">
          <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-transparent">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div>
                <h2 class="font-bold text-gray-800">Oturumlar</h2>
                <p class="text-xs text-gray-500">Bugünü bulup seçmek için listeyi kullan</p>
              </div>
            </div>
          </div>

          <div class="p-4 space-y-2 max-h-[520px] overflow-auto">
            <button
              v-for="s in sessions"
              :key="s.id"
              class="w-full p-3 rounded-xl border-2 transition-all duration-200 text-left"
              :class="selectedSessionId === s.id 
                ? 'border-primary bg-primary/5 shadow-sm' 
                : 'border-gray-100 hover:border-gray-200 hover:bg-gray-50'"
              @click="selectSession(s.id)"
            >
              <div class="flex items-center justify-between gap-3">
                <div class="flex-1 min-w-0">
                  <div class="font-semibold text-gray-800 text-sm truncate">{{ formatDT(s.starts_at) }}</div>
                  <div class="text-xs text-gray-500 mt-1 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    {{ s.attendance_count }} kayıt
                  </div>
                </div>
                <span 
                  class="badge text-xs"
                  :class="s.is_open ? 'badge-success text-white' : 'badge-ghost'"
                >
                  {{ s.is_open ? "Açık" : "Kapalı" }}
                </span>
              </div>
            </button>

            <div v-if="sessions.length === 0 && !loading" class="p-8 text-center">
              <div class="flex flex-col items-center gap-2 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span class="text-sm">Oturum yok</span>
                <span class="text-xs">Program ekleyip "Oturumları Oluştur" ile üretin</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Session Detail Card -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden lg:col-span-2">
          <div v-if="!selectedSessionId" class="h-full flex items-center justify-center p-12">
            <div class="text-center">
              <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-800 mb-2">Oturum Seçin</h3>
              <p class="text-gray-500 text-sm">Soldaki listeden detaylarını görmek istediğiniz oturumu seçin</p>
            </div>
          </div>

          <div v-else>
            <!-- Session Header -->
            <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-green-50 to-transparent">
              <div class="flex items-center justify-between gap-4 flex-wrap">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center" :class="sessionDetail?.is_open ? 'bg-green-100' : 'bg-gray-100'">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="sessionDetail?.is_open ? 'text-green-600' : 'text-gray-500'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path v-if="sessionDetail?.is_open" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                      <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <div>
                    <div class="flex items-center gap-2">
                      <h2 class="font-bold text-gray-800">Oturum #{{ selectedSessionId }}</h2>
                      <span class="badge" :class="sessionDetail?.is_open ? 'badge-success text-white' : 'badge-ghost'">
                        {{ sessionDetail?.is_open ? "Açık" : "Kapalı" }}
                      </span>
                    </div>
                    <p class="text-xs text-gray-500">{{ sessionDetail?.starts_at }} → {{ sessionDetail?.ends_at }}</p>
                  </div>
                </div>

                <div class="flex flex-wrap gap-2">
                  <button 
                    class="btn btn-success btn-sm gap-1" 
                    :disabled="loading || sessionDetail?.is_open" 
                    @click="toggleOpen(true)"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                    </svg>
                    Aç
                  </button>
                  <button 
                    class="btn btn-warning btn-sm gap-1" 
                    :disabled="loading || !sessionDetail?.is_open" 
                    @click="toggleOpen(false)"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                    Kapat
                  </button>
                  <button class="btn btn-ghost btn-sm gap-1" :disabled="loading" @click="refreshSelectedSession">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Yenile
                  </button>
                </div>
              </div>
            </div>

            <!-- Session Content -->
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
                        <img :src="qr.image_data_url" alt="QR" class="w-full max-w-[200px]" />
                      </div>

                      <div class="text-center space-y-2">
                        <div class="flex items-center justify-center gap-2 text-sm">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span>Süre: <b class="text-primary">{{ qrSecondsLeft ?? qr.expires_in }}</b> sn</span>
                        </div>
                        <p class="text-xs text-gray-500">Otomatik yenileme aktif ✅</p>
                      </div>

                      <button class="btn btn-primary btn-sm w-full gap-2" :disabled="loading" @click="refreshQr">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        QR Yenile
                      </button>
                    </div>

                    <div v-else class="py-8 text-center">
                      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                      </div>
                      <p class="text-sm text-gray-500">QR göstermek için oturumu açın</p>
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
                      <span class="badge badge-primary">{{ (sessionDetail?.attendance || []).length }}</span>
                    </div>
                  </div>

                  <div class="p-4 max-h-[400px] overflow-auto">
                    <div v-if="(sessionDetail?.attendance || []).length === 0" class="py-8 text-center">
                      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </div>
                      <p class="text-sm text-gray-500">Henüz yoklama kaydı yok</p>
                    </div>

                    <div v-else class="space-y-2">
                      <div 
                        v-for="a in sessionDetail?.attendance || []" 
                        :key="a.attendance_id"
                        class="bg-white rounded-lg p-3 border border-gray-100 hover:border-gray-200 transition-colors"
                      >
                        <div class="flex items-center justify-between gap-3">
                          <div class="flex items-center gap-3 min-w-0">
                            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center shrink-0">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                              </svg>
                            </div>
                            <div class="min-w-0">
                              <div class="font-medium text-gray-800 truncate">{{ a.student_name }}</div>
                              <div class="text-xs text-gray-500 truncate">{{ a.student_email }}</div>
                            </div>
                          </div>
                          <div class="text-right shrink-0">
                            <span class="badge badge-success badge-outline text-xs">{{ a.status }}</span>
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

// Announcements
const announcements = ref<any[]>([]);
const annTitle = ref<string>("");
const annContent = ref<string>("");

async function loadAnnouncements() {
  try {
    const api = await getApi();
    const resp = await api.get(`/api/instructor/offerings/${offeringId.value}/announcements`);
    announcements.value = resp.data.items || [];
  } catch (e) {
    console.error("Duyurular yüklenemedi", e);
  }
}

async function addAnnouncement() {
  if (!annTitle.value.trim()) return;
  loading.value = true;
  errorMsg.value = null;
  try {
    const api = await getApi();
    await api.post(`/api/instructor/offerings/${offeringId.value}/announcements`, {
      title: annTitle.value.trim(),
      content: annContent.value.trim(),
    });
    annTitle.value = "";
    annContent.value = "";
    await loadAnnouncements();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Duyuru eklenemedi");
  } finally {
    loading.value = false;
  }
}

async function deleteAnnouncement(id: number) {
  loading.value = true;
  errorMsg.value = null;
  try {
    const api = await getApi();
    await api.delete(`/api/instructor/announcements/${id}`);
    await loadAnnouncements();
  } catch (e: any) {
    errorMsg.value = String(e?.response?.data?.details || e?.response?.data?.error || e?.message || "Duyuru silinemedi");
  } finally {
    loading.value = false;
  }
}

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
    await loadAnnouncements();
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
