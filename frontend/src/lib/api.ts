import axios, { AxiosError } from 'axios';

// Determine API base URL at runtime. Vite exposes variables prefixed with VITE_.
// When running behind the dev proxy we keep the "/api" prefix so that requests
// are forwarded. In production we default to the full backend URL.
const baseURL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}` : '/api';

export const api = axios.create({ baseURL });

// Request interceptor to add JWT token
api.interceptors.request.use((config) => {
  // Do not attach token when hitting auth endpoints
  if (config.url?.includes('/token/')) {
    return config;
  }

  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }
        
        const response = await axios.post(`${baseURL}/token/refresh/`, {
          refresh: refreshToken,
        });
        
        const { access, refresh: newRefresh } = response.data as {
          access: string;
          refresh?: string;
        };
        localStorage.setItem('token', access);
        if (newRefresh) {
          localStorage.setItem('refreshToken', newRefresh);
        }
        
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Helper for typed fetch calls (alternative to axios)
export async function typedFetch<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${baseURL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

// Extend axios config type to include retry flag
declare module 'axios' {
  interface AxiosRequestConfig {
    _retry?: boolean;
  }
}
