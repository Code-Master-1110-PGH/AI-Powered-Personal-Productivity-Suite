/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#070A12',
        surface: {
          50: '#141A28',
          100: '#101623',
          200: '#0C111C',
          300: '#090D16',
        },
        border: {
          subtle: 'rgba(255, 255, 255, 0.08)',
          glow: 'rgba(56, 189, 248, 0.35)',
        },
        neon: {
          cyan: '#00F0FF',
          blue: '#38BDF8',
          purple: '#A855F7',
          violet: '#8B5CF6',
          pink: '#F43F5E',
          emerald: '#10B981',
          mint: '#00F5A0',
          amber: '#F59E0B',
        },
      },
      boxShadow: {
        'glow-cyan': '0 0 25px -4px rgba(0, 240, 255, 0.45)',
        'glow-purple': '0 0 25px -4px rgba(168, 85, 247, 0.45)',
        'glow-emerald': '0 0 25px -4px rgba(16, 185, 129, 0.45)',
        'glow-subtle': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan': 'scan 2.5s ease-in-out infinite',
      },
      keyframes: {
        scan: {
          '0%, 100%': { transform: 'translateY(0%)', opacity: 0.2 },
          '50%': { transform: 'translateY(100%)', opacity: 0.8 },
        },
      },
    },
  },
  plugins: [],
};

