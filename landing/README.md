# PriceCheck Landing Page

Marketing landing page for the PriceCheck Chrome extension.

## Structure

6 sections per PRD:
1. **Hero** - Main headline and CTAs
2. **Trust Bar** - 4 key stats
3. **Demo Result** - Example analysis (DreamCloud mattress)
4. **How It Works** - 3-step process
5. **Tactic Cards** - 6 detection categories
6. **Bottom CTA** - Final install prompt

## Development

Install dependencies:
```bash
npm install
```

Run dev server:
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Deployment

Built files go to `dist/` folder. Deploy to Netlify or any static hosting.

## Design System

Uses same design tokens as extension:
- Colors: red-alarm, paper, ink, trust, amber
- Fonts: Barlow Condensed (display), Libre Franklin (body), JetBrains Mono (mono)
- Fully responsive (tested at 375px mobile width)

## Copy Rule

No em dashes in any user-facing text. Use commas, colons, or rewrite instead.
