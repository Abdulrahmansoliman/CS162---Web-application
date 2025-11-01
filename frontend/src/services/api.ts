/**
 * Base API client configuration with axios
 * Handles authentication, error handling, and request/response interceptors
 */

import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for session cookies
  timeout: 10000, // 10 seconds
});

// Request interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // You can add auth tokens here if switching to JWT
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data: any = error.response.data;

      switch (status) {
        case 401:
          // Unauthorized - redirect to login or clear session
          console.error('Unauthorized access - please login');
          break;
        case 403:
          console.error('Forbidden - insufficient permissions');
          break;
        case 404:
          console.error('Resource not found');
          break;
        case 500:
          console.error('Server error');
          break;
        default:
          console.error(`Error ${status}:`, data.error || 'Unknown error');
      }

      return Promise.reject({
        status,
        message: data.error || 'An error occurred',
      });
    } else if (error.request) {
      // Request made but no response
      console.error('Network error - no response from server');
      return Promise.reject({
        status: 0,
        message: 'Network error - please check your connection',
      });
    } else {
      // Something else happened
      console.error('Error:', error.message);
      return Promise.reject({
        status: 0,
        message: error.message || 'An unexpected error occurred',
      });
    }
  }
);

export default apiClient;
