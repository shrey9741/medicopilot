import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  token: localStorage.getItem('medicopilot_token') || null,
  doctor: JSON.parse(localStorage.getItem('medicopilot_doctor') || 'null'),

  login: (token, doctor) => {
    localStorage.setItem('medicopilot_token', token);
    localStorage.setItem('medicopilot_doctor', JSON.stringify(doctor));
    set({ token, doctor });
  },

  logout: () => {
    localStorage.removeItem('medicopilot_token');
    localStorage.removeItem('medicopilot_doctor');
    set({ token: null, doctor: null });
  },
}));