/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, { AxiosError, AxiosResponse } from 'axios';
import { toast } from 'sonner';

// Types
interface ErrorResponse {
  message: string;
  status: number;
}

// Create axios instance
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    // const token = localStorage.getItem('token');
    
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError<ErrorResponse>) => {
    const errorMessage = error.response?.data?.message || 'An unexpected error occurred';
    const errorStatus = error.response?.status;

    // Handle different error scenarios
    switch (errorStatus) {
      case 401:
        toast.error('Session expired. Please login again.');
        // Add logout logic or redirect to login
        break;
      case 403:
        toast.error('You do not have permission to perform this action');
        break;
      case 404:
        toast.error('Resource not found');
        break;
      case 500:
        toast.error('Server error. Please try again later');
        break;
      default:
        toast.error(errorMessage);
    }

    return Promise.reject(error);
  }
);

// API wrapper functions for type safety
export const apiService = {
  get: <T>(url: string, params?: any) => 
    api.get<T>(url, { params }).then(response => response.data),
    
  post: <T>(url: string, data: any) => 
    api.post<T>(url, data).then(response => response.data),
    
  put: <T>(url: string, data: any) => 
    api.put<T>(url, data).then(response => response.data),
    
  delete: <T>(url: string) => 
    api.delete<T>(url).then(response => response.data),
};