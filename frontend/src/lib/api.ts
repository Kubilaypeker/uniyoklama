import axios, { type AxiosInstance } from "axios";
import { getBackendBaseUrl } from "../config";

let instance: AxiosInstance | null = null;

export async function getApi(): Promise<AxiosInstance> {
  if (instance) return instance;

  const baseURL = await getBackendBaseUrl();
  instance = axios.create({
    baseURL,
    timeout: 15000,
  });

  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  });

  return instance;
}
