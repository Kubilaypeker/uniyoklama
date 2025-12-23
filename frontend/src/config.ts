export type AppConfig = {
  backendBaseUrl: string;
};

let cached: AppConfig | null = null;

export async function loadConfig(): Promise<AppConfig> {
  if (cached) return cached;

  const resp = await fetch("/app-config.json", { cache: "no-store" });
  if (!resp.ok) throw new Error("app-config.json okunamadı");
  const data = (await resp.json()) as AppConfig;

  if (!data.backendBaseUrl) throw new Error("backendBaseUrl eksik");
  cached = data;
  return data;
}

export async function getBackendBaseUrl(): Promise<string> {
  const cfg = await loadConfig();
  return cfg.backendBaseUrl.replace(/\/$/, "");
}
