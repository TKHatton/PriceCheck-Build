# Landing Page Setup & Testing

## ✓ Landing Page Built

All 6 sections implemented per PRD Part 6.4.

---

## Quick Start

**Install dependencies:**
```bash
cd landing
npm install
```

**Run development server:**
```bash
npm run dev
```

This will open at `http://localhost:5173`

---

## Sections Implemented

### 1. Hero (Above the fold)
- **Headline:** "YOU THINK YOU ARE GETTING A DEAL" (large, Barlow Condensed 800)
- **Line 2:** "PriceCheck finds out the truth." (red)
- **CTAs:**
  - "Install Extension" (red-alarm background)
  - "See How It Works" (outline button)

### 2. Trust Bar
- One line, 4 stats separated by dots
- JetBrains Mono, ink-light color
- Stats: Works on any product page, 6 manipulation categories, Fake site detection, Gaslighting Score 0-100
- Responsive: stacks on mobile, inline with dots on desktop

### 3. Demo Result
- **Label:** "Example Analysis"
- **Two-column layout:**
  - Left (white): "WHAT THEY SHOW" - DreamCloud mattress, $499, fake discount
  - Right (red-tint): "WHAT IS REALLY HAPPENING" - $1,127 real price, 3 hidden fees listed
- **Score badge below:** 74/100, "Full Gaslighting"
- Responsive: stacks on mobile, side-by-side on desktop (md breakpoint)

### 4. How It Works
- **3 numbered steps:**
  1. Install the extension
  2. Visit any product page
  3. Click the icon
- Red numbered circles (1, 2, 3)
- Horizontal on desktop, stacked on mobile
- Short, no paragraphs

### 5. Tactic Cards
- **6 cards for detection categories:**
  1. Fake Discounts
  2. Hidden Fees
  3. Drip Pricing
  4. Dark Patterns
  5. Subscription Traps
  6. Shrinkflation
- Red left border, white background
- Grid layout: 3 columns desktop, 2 tablet, 1 mobile
- Each card has category name and description

### 6. Bottom CTA
- Red-alarm background (full width)
- Tagline: "Stop getting played."
- Install Extension button (white background)

---

## Design System

### Colors
- Red alarm: #D42B2B
- Red tint: #FDF1F1
- Red mid: #F5C5C5
- Paper: #FAF9F6
- Ink: #1C1B18
- Ink mid: #4A4845
- Ink light: #8C8880

### Fonts
- Display: Barlow Condensed (headlines, buttons, numbers)
- Body: Libre Franklin (readable content)
- Mono: JetBrains Mono (stats, labels)

### Responsive Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1023px
- Desktop: 1024px+

---

## Testing Checklist

### Desktop (1280px+)
- [ ] Hero headline large and impactful
- [ ] Two CTAs side by side
- [ ] Trust bar stats inline with dots
- [ ] Demo result: two columns side by side
- [ ] How It Works: 3 steps horizontal
- [ ] Tactic cards: 3 columns
- [ ] Bottom CTA centered

### Tablet (768px)
- [ ] Hero still readable
- [ ] CTAs stack vertically
- [ ] Demo result: columns stack
- [ ] How It Works: 3 steps horizontal or stacked
- [ ] Tactic cards: 2 columns

### Mobile (375px) - CRITICAL TEST
- [ ] Hero text scales down but readable
- [ ] CTAs full width, stacked
- [ ] Trust bar stats stack or wrap nicely
- [ ] Demo sections stack (white, then red-tint)
- [ ] How It Works: 3 steps stacked
- [ ] Tactic cards: 1 column
- [ ] Everything readable and tappable

---

## Copy Compliance

✓ **No em dashes used** - Per PRD copy rule
✓ All text uses commas or colons instead

---

## Build for Production

```bash
cd landing
npm run build
```

Output goes to `landing/dist/` - ready to deploy to Netlify.

---

## What to Check

### Visual Hierarchy
1. Hero grabs attention immediately
2. Trust bar builds credibility
3. Demo shows the product in action
4. How It Works is dead simple
5. Tactic cards show depth
6. CTA is clear final action

### Content
- Headlines punchy and clear
- No jargon or complexity
- CTAs obvious and actionable
- Demo example is concrete (real mattress scenario)

### Performance
- Loads fast (no heavy images yet)
- Animations smooth
- Responsive at all sizes
- Touch targets big enough on mobile

---

## Next Steps

After reviewing:
1. Add demo video embed if needed
2. Replace #install with Chrome Web Store link
3. Add analytics tracking
4. Deploy to Netlify

Current state: **All 6 sections built, ready to preview**
