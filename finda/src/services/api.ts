import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const API_TIMEOUT = 10000; // 10 seconds

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
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
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    
    if (error.response?.status === 403) {
      // Forbidden
      console.error('Access forbidden');
    }
    
    if (error.response?.status >= 500) {
      // Server error
      console.error('Server error occurred');
    }
    
    return Promise.reject(error);
  }
);

// API response types
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Generic API methods
export const api = {
  get: <T = any>(url: string, config?: AxiosRequestConfig) =>
    apiClient.get<ApiResponse<T>>(url, config).then(res => res.data),
    
  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.post<ApiResponse<T>>(url, data, config).then(res => res.data),
    
  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.put<ApiResponse<T>>(url, data, config).then(res => res.data),
    
  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig) =>
    apiClient.patch<ApiResponse<T>>(url, data, config).then(res => res.data),
    
  delete: <T = any>(url: string, config?: AxiosRequestConfig) =>
    apiClient.delete<ApiResponse<T>>(url, config).then(res => res.data),
};

// Specific API endpoints
export const userApi = {
  getUsers: (params?: { page?: number; limit?: number; search?: string }) =>
    api.get<PaginatedResponse<any>>('/users', { params }),
    
  getUser: (id: string) =>
    api.get<any>(`/users/${id}`),
    
  createUser: (userData: any) =>
    api.post<any>('/users', userData),
    
  updateUser: (id: string, userData: any) =>
    api.put<any>(`/users/${id}`, userData),
    
  deleteUser: (id: string) =>
    api.delete(`/users/${id}`),
};

export const companyApi = {
  getCompanies: (params?: { page?: number; limit?: number; search?: string }) =>
    api.get<PaginatedResponse<any>>('/companies', { params }),
    
  getCompany: (id: string) =>
    api.get<any>(`/companies/${id}`),
    
  createCompany: (companyData: any) =>
    api.post<any>('/companies', companyData),
    
  updateCompany: (id: string, companyData: any) =>
    api.put<any>(`/companies/${id}`, companyData),
    
  deleteCompany: (id: string) =>
    api.delete(`/companies/${id}`),
};

export default apiClient;
