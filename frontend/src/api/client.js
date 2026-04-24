import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('medicopilot_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

API.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('medicopilot_token');
      localStorage.removeItem('medicopilot_doctor');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default API;