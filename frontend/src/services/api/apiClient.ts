import axios, { AxiosInstance, AxiosError, AxiosResponse } from 'axios';
import useAuthStore from '@store/authStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const accessToken = useAuthStore.getState().accessToken;
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest: any = error.config;
    
    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = useAuthStore.getState().refreshToken;
        if (refreshToken) {
          // TODO: Implement token refresh logic
          // const response = await refreshAccessToken(refreshToken);
          // useAuthStore.getState().setAuth(response.data.user, response.data.access_token, response.data.refresh_token);
          // return apiClient(originalRequest);
        }
      } catch (refreshError) {
        useAuthStore.getState().logout();
        window.location.href = '/login';
      }
    }

    // Handle other errors
    if (error.response?.status === 403) {
      console.error('Permission denied');
    }

    if (error.response?.status === 500) {
      console.error('Server error');
    }

    return Promise.reject(error);
  }
);

export default apiClient;

// Helper functions for common HTTP methods
export const api = {
  get: <T = any>(url: string, config?: any): Promise<AxiosResponse<T>> => 
    apiClient.get(url, config),
  
  post: <T = any>(url: string, data?: any, config?: any): Promise<AxiosResponse<T>> => 
    apiClient.post(url, data, config),
  
  put: <T = any>(url: string, data?: any, config?: any): Promise<AxiosResponse<T>> => 
    apiClient.put(url, data, config),
  
  patch: <T = any>(url: string, data?: any, config?: any): Promise<AxiosResponse<T>> => 
    apiClient.patch(url, data, config),
  
  delete: <T = any>(url: string, config?: any): Promise<AxiosResponse<T>> => 
    apiClient.delete(url, config),
};