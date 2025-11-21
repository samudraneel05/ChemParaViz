import axios from 'axios';

// Use environment variable for API URL, fallback to localhost
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (username, password, email) =>
    api.post('/auth/register/', { username, password, email }),
  login: (username, password) =>
    api.post('/auth/login/', { username, password }),
};

// Dataset APIs
export const datasetAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getAll: () => api.get('/datasets-list/'),
  getDetail: (id) => api.get(`/dataset/${id}/`),
  delete: (id) => api.delete(`/dataset/${id}/delete/`),
  downloadReport: (id) => 
    api.get(`/dataset/${id}/report/`, { responseType: 'blob' }),
  getHistory: () => api.get('/history/'),
};

export default api;
