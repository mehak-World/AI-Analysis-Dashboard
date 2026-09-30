// api/apiClient.ts
import axios, { AxiosError } from "axios";
import type { InternalAxiosRequestConfig } from "axios";
import { ENV } from "../config/env";
import { tokenStore } from "../modules/auth/tokenStore";

// Extend the config type so TypeScript knows about our custom _retry flag
interface RetryableRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

const apiClient = axios.create({
  baseURL: "/api",
  withCredentials: true, // sends the httpOnly refreshToken cookie automatically
});

// --- Request interceptor: attach access token ---
apiClient.interceptors.request.use((config) => {
  const token = tokenStore.getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Queue so concurrent 401s trigger only ONE refresh call ---
let isRefreshing = false;
let pendingQueue: {
  resolve: (token: string) => void;
  reject: (err: unknown) => void;
}[] = [];

const flushQueue = (error: unknown, token: string | null) => {
  pendingQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error);
    else resolve(token!);
  });
  pendingQueue = [];
};

// --- Response interceptor: handle 401 -> refresh -> retry ---
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetryableRequestConfig;

    // Never try to "refresh the refresh" — that's what caused the redirect loop
    const isRefreshCall = originalRequest?.url?.includes("/auth/refresh");

    if (
      error.response?.status !== 401 ||
      originalRequest._retry ||
      isRefreshCall
    ) {
      return Promise.reject(error);
    }

    if (isRefreshing) {
      // A refresh is already in flight — queue this request instead of
      // firing a second /auth/refresh call
      return new Promise((resolve, reject) => {
        pendingQueue.push({
          resolve: (token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(apiClient(originalRequest));
          },
          reject,
        });
      });
    }

    originalRequest._retry = true;
    isRefreshing = true;

    try {
      // Plain axios, not apiClient — must not pass through this same interceptor
      const { data } = await axios.get(`${ENV.API_BASE_URL}/auth/refresh`, {
        withCredentials: true,
      });

      tokenStore.setAccessToken(data.data.accessToken);
      flushQueue(null, data.data.accessToken);

      originalRequest.headers.Authorization = `Bearer ${data.data.accessToken}`;
      return apiClient(originalRequest);
    } catch (refreshError) {
      flushQueue(refreshError, null);
      tokenStore.clearAccessToken();

      // Guard against redirecting to where we already are
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }

      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default apiClient;