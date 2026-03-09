import axios from 'axios';

// 🎯 The baseURL is '/api' to match the Vite proxy in your vite.config.ts
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'X-API-KEY': import.meta.env.VITE_API_KEY // 🛡️ Replace with your real secret key
  },
});

// Optional: Global error interceptor to catch 403 Forbidden errors instantly
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 403) {
      console.error('🚫 API Key Denied. Double-check your backend security settings.');
    }
    return Promise.reject(error);
  }
);

export default api;
