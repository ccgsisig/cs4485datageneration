import { Config } from "tailwindcss";
import colors from "tailwindcss/colors";

const config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        inherit: colors.inherit,
        current: colors.current,
        transparent: colors.transparent,
        primary: "#1A202C", // Darker shade for primary
        secondary: "#FF6347", // Tomato red for secondary
        info: "#4682B4", // SteelBlue for info
        black: colors.black,
        white: colors.white,
        slate: colors.slate,
        gray: {
          50: "#F8F9FA", // Lighter gray
          100: "#E0E0E0", // Light gray
          200: "#B8B8B8", // Medium light gray
          300: "#888888", // Neutral gray
          400: "#666666", // Darker gray
          500: "#444444", // Dark gray
          600: "#333333", // Very dark gray
          700: "#1F1F1F", // Almost black gray
          800: "#141414", // Very dark
          900: "#0A0A0A", // Black gray
        },
        zinc: colors.zinc,
        neutral: colors.neutral,
        stone: colors.stone,
        red: colors.red,
        orange: "#FFA500", // Orange color
        amber: "#FFD700", // Amber color
        yellow: "#FFDD00", // Bright Yellow
        lime: "#32CD32", // Lime Green
        green: "#28A745", // Green color
        emerald: "#2E8B57", // Emerald Green
        teal: "#20B2AA", // Light Teal
        cyan: "#00FFFF", // Cyan color
        sky: "#87CEEB", // Sky Blue
        blue: "#1E90FF", // Dodger Blue
        indigo: "#4B0082", // Indigo color
        violet: "#EE82EE", // Violet color
        purple: "#800080", // Purple color
        fuchsia: "#FF00FF", // Fuchsia color
        pink: "#FFC0CB", // Pink color
        rose: "#FF007F", // Rose color
        charcoal: "#2F4F4F", // Charcoal color
        electricblue: "#10B981", // Neon Green
        vibrantgreen: "#00FF00", // Vibrant Green
        subtlegray: "#D3D3D3", // Subtle Gray
        lightgray: "#E0E0E0", // Light Gray
        darkerblue: "#4B6A8C", // Darker Blue
      },
    },
  },
  plugins: [],
};

export default config;
