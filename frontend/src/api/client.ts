import axios from 'axios';
import type { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8002';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const authAPI = {
  login: (email: string, password: string) => {
    const form = new URLSearchParams();
    form.append('username', email);
    form.append('password', password);
    return apiClient.post('/api/v1/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
  register: (email: string, password: string) =>
    apiClient.post('/api/v1/auth/register', { email, password }),
};

// Collections endpoints
export const collectionsAPI = {
  getAll: () => apiClient.get('/api/v1/collections/'),
  create: (data: { name: string; slug: string; description?: string }) =>
    apiClient.post('/api/v1/collections/', data),
  getFields: (collectionId: string) =>
    apiClient.get(`/api/v1/collections/${collectionId}/fields`),
  createField: (collectionId: string, data: any) =>
    apiClient.post(`/api/v1/collections/${collectionId}/fields`, data),
  delete: (collectionId: string) =>
    apiClient.delete(`/api/v1/collections/${collectionId}`),
  deleteField: (collectionId: string, fieldId: string) =>
    apiClient.delete(`/api/v1/collections/${collectionId}/fields/${fieldId}`),
};

// Content endpoints
export const contentAPI = {
  getByCollection: (collectionSlug: string, params?: any) =>
    apiClient.get(`/api/v1/content/${collectionSlug}`, { params }),
  create: (collectionSlug: string, data: any) =>
    apiClient.post(`/api/v1/content/${collectionSlug}`, data),
  update: (collectionSlug: string, contentId: string, data: any) =>
    apiClient.put(`/api/v1/content/${collectionSlug}/${contentId}`, data),
  delete: (collectionSlug: string, contentId: string) =>
    apiClient.delete(`/api/v1/content/${collectionSlug}/${contentId}`),
};

// Media endpoints
export const mediaAPI = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/api/v1/media/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  delete: (mediaId: string) => apiClient.delete(`/api/v1/media/${mediaId}`),
};

// Health check
export const healthAPI = {
  check: () => apiClient.get('/health'),
};

export default apiClient;
