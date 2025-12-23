<template>
  <div class="card bg-base-100 shadow-sm">
    <div class="card-body">
      <div class="flex items-center justify-between">
        <h2 class="card-title">Katılım Geçmişim</h2>
        <button class="btn btn-sm btn-primary" :disabled="loading" @click="load">
          Yenile
        </button>
      </div>

      <div v-if="errorMsg" class="alert alert-warning">
        <span>{{ errorMsg }}</span>
      </div>

      <div class="overflow-x-auto">
        <table class="table table-sm">
          <thead>
            <tr>
              <th>ID</th>
              <th>Session</th>
              <th>Durum</th>
              <th>Okutma</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="it in items" :key="it.id">
              <td>{{ it.id }}</td>
              <td>{{ it.session_id }}</td>
              <td><span class="badge badge-outline">{{ it.status }}</span></td>
              <td class="text-xs opacity-70">{{ it.scanned_at || "-" }}</td>
            </tr>
            <tr v-if="items.length === 0 && !loading">
              <td colspan="4" class="text-center text-sm opacity-70">Kayıt yok.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getApi } from "../lib/api";

const items = ref<any[]>([]);
const loading = ref(false);
const errorMsg = ref<string | null>(null);

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
