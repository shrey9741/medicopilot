/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#003178",
        "primary-container": "#0d47a1",
        "primary-fixed": "#d9e2ff",
        "primary-fixed-dim": "#b0c6ff",
        "on-primary": "#ffffff",
        "surface": "#f8f9fb",
        "surface-container-low": "#f2f4f6",
        "surface-container-high": "#e6e8ea",
        "on-surface": "#191c1e",
        "on-surface-variant": "#434652",
        "error": "#ba1a1a",
        "error-container": "#ffdad6",
      },
      fontFamily: {
        headline: ["Manrope", "sans-serif"],
        body: ["Inter", "sans-serif"],
        label: ["Inter", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.125rem",
        lg: "0.25rem",
        xl: "0.5rem",
        full: "0.75rem",
      },
    },
  },
  plugins: [],
}