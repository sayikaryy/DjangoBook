// src/utils/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true, // needed if you're using cookies (optional with tokens)
});

// Request interceptor: attach access token if available
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => Promise.reject(error)
);

// Response interceptor: auto-refresh token if access is expired
instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // If 401 and we haven't retried yet
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refresh')
    ) {
      originalRequest._retry = true;
      try {
        // Refresh token
        const res = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
          refresh: localStorage.getItem('refresh'),
        });

        // Save new access token
        localStorage.setItem('access', res.data.access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
        return instance(originalRequest);
      } catch (refreshErr) {
        console.error('🔁 Token refresh failed:', refreshErr);
        // Clear tokens and redirect to login
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default instance;
