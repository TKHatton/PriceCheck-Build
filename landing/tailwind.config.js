/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'red-alarm':   '#D42B2B',
        'red-tint':    '#FDF1F1',
        'red-mid':     '#F5C5C5',
        'amber':       '#C47C00',
        'amber-tint':  '#FDF6E8',
        'trust':       '#1A7A4A',
        'trust-tint':  '#EDF7F2',
        'ink':         '#1C1B18',
        'ink-mid':     '#4A4845',
        'ink-light':   '#8C8880',
        'paper':       '#FAF9F6',
        'rule':        '#E2E0DA',
      },
      fontFamily: {
        'display': ["'Barlow Condensed'", 'sans-serif'],
        'body':    ["'Libre Franklin'", 'sans-serif'],
        'mono':    ["'JetBrains Mono'", 'monospace'],
      },
    },
  },
  plugins: [],
}
