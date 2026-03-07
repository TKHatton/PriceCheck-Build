/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx,html}",
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
      transitionTimingFunction: {
        'reveal': 'cubic-bezier(0.16, 1, 0.3, 1)',
        'snap': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      transitionDuration: {
        'hover': '150ms',
        'card': '500ms',
        'score': '1200ms',
      },
    },
  },
  plugins: [],
}
