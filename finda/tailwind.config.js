export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  cssEngine: "v4",
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#fff7ed",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
        },
        gray: {
          50: "#f9fafb",
          100: "#f3f4f6",
          900: "#111827",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      spacing: {
        18: "4.5rem",
        88: "22rem",
      },
    },
    screens: {
      mobile: "320px",
      tablet: "768px",
      desktop: "1024px",
      xl: "1280px",
    },
  },
  plugins: [],
};

