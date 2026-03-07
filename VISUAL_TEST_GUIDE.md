# PriceCheck Visual Testing Guide

## ✓ Build Complete - Ready to Test

Extension rebuilt with all UI components. Here's what you should see and how to test it.

---

## Components Built

1. **LoadingNarrative** - Sequential loading steps with 700ms stagger
2. **ScoreDisplay** - Animated score count-up with dynamic colors
3. **TacticCard** - Individual manipulation tactic display
4. **SplitScreen** - Price comparison and tactic list
5. **TrustBadge** - Domain trust indicator
6. **ResultsView** - Orchestrates full results display

---

## How to Test

### Step 1: Reload Extension

1. Go to `chrome://extensions/`
2. Find PriceCheck
3. Click refresh icon (circular arrow on the card)

### Step 2: Open Test Page

Open in Chrome: `test-page.html`

### Step 3: Open DevTools (Important!)

Press `F12` to open DevTools and click Console tab

### Step 4: Click Extension Icon

Click the red PriceCheck icon in toolbar

### Step 5: Click "Analyze This Page"

Watch the popup transform through these states:

---

## What You Should See

### 🔄 Loading State (First 2-3 seconds)

**In the popup:**
- Button changes to "Analyzing..." and becomes disabled
- Below the button, text appears sequentially:
  ```
  Reading this page...
  Checking domain trust...        (appears after 0.7s)
  Analyzing pricing tactics...    (appears after 1.4s)
  Calculating your Gaslighting Score...  (appears after 2.1s)
  ```

**Font:** JetBrains Mono (monospace)
**Color:** Gray-ish (ink-mid)
**Animation:** Each line fades in smoothly

---

### 📊 Results State (After ~3-5 seconds)

The loading text disappears and you see (from top to bottom):

#### 1. Trust Badge
- Green box with "DOMAIN VERIFIED" (if trust = 100)
- Or amber/red if trust issues detected
- Shows "Trust: 100/100"

#### 2. What They Show Section
- White box with label "WHAT THEY SHOW"
- Page title: "Test Product - Amazing Deal!"
- Price: $79.99 (if detected)

#### 3. What Is Really Happening Section
- Light red background (red-tint)
- Label "WHAT IS REALLY HAPPENING"
- Real price, price delta if applicable

#### 4. Manipulation Tactics Section
- Label: "MANIPULATION TACTICS DETECTED"
- 3 tactic cards appear one by one (80ms apart):

  **Card 1:** FAKE DISCOUNT (red border, red background)
  - Evidence in quotes (italic, small monospace)
  - Explanation in body font

  **Card 2:** DARK PATTERNS (red border, red background)
  - "SALE ENDS IN 09:47! Only 3 left!"
  - Explanation about false urgency

  **Card 3:** SUBSCRIPTION TRAP (amber border, amber background)
  - "Free trial, cancel anytime $49/month after"
  - Explanation about auto-conversion

#### 5. Gaslighting Score (Center, Bottom)
- Big number with red border and shadow
- **Counts up from 0 → 24** over 1.2 seconds
- Number color changes based on score:
  - Green (0-20)
  - Amber (21-45) ← Should be amber for score ~24
  - Red (46+)
- Below number: "MILDLY MISLEADING" in uppercase
- "/100" in lighter gray

---

## Visual Details to Check

### Colors
- **Red borders:** Bright red (#D42B2B)
- **Red backgrounds:** Very light pink (#FDF1F1)
- **Amber borders:** Orange (#C47C00)
- **Green:** Forest green (#1A7A4A)
- **Page background:** Warm off-white (#FAF9F6)

### Fonts
- **Title "PriceCheck":** Barlow Condensed (condensed sans)
- **Score number:** Barlow Condensed (very bold)
- **Tactic names:** Barlow Condensed uppercase
- **Loading text & evidence:** JetBrains Mono (monospace)
- **Body text:** Libre Franklin (clean sans)

### Animations
- **Loading steps:** Fade in sequentially, smooth transitions
- **Tactic cards:** Slide in from left, one after another
- **Score number:** Counts up smoothly (not jumping)
- **Overall:** Should feel polished and intentional

### Layout
- **Popup width:** 400px fixed
- **Spacing:** Clean margins between sections
- **Scrollable:** If content is long, popup should scroll
- **Score:** Centered, prominent

---

## Expected Flow Timeline

```
0.0s  - Click "Analyze This Page"
0.0s  - Button → "Analyzing..."
0.0s  - "Reading this page..." appears
0.7s  - "Checking domain trust..." appears
1.4s  - "Analyzing pricing tactics..." appears
2.1s  - "Calculating your Gaslighting Score..." appears
3-5s  - Results appear (loading text disappears)
3.0s  - Trust badge fades in
3.0s  - Price sections appear
3.0s  - First tactic card slides in
3.08s - Second tactic card slides in
3.16s - Third tactic card slides in
3.2s  - Score badge appears
3.2s  - Score starts counting 0 → 24
4.4s  - Score finishes at 24
```

Total experience: ~4-5 seconds with smooth animations throughout

---

## Console Output to Check

```
PriceCheck content script loaded
[Popup] Page data extracted: {url: "file://...", title: "Test Product...", ...}
[Popup] Full analysis result: {...}
[Popup] Gaslighting score: 24
[Popup] Severity label: "Mildly Misleading"
[Popup] Tactics found: 3
[Popup] Trust score: 100
[Popup] Is scam: false
```

---

## What Good Looks Like

✓ Smooth, professional animations
✓ Clear color coding (red = bad, green = good)
✓ Easy to read fonts and sizing
✓ Loading state feels purposeful, not just a spinner
✓ Results are scannable at a glance
✓ Tactic cards clearly show what was detected
✓ Score is the hero element (big, centered, animated)

---

## What to Look For (Give Feedback On)

1. **Pacing:** Do the animations feel too fast/slow?
2. **Colors:** Are severity indicators clear enough?
3. **Text sizes:** Is anything too small to read?
4. **Layout:** Does it feel cramped or is spacing good?
5. **Score animation:** Does the count-up feel satisfying?
6. **Overall feel:** Does it feel professional and credible?

---

## Files Updated

- `extension/src/components/TacticCard.jsx` (NEW)
- `extension/src/components/SplitScreen.jsx` (NEW)
- `extension/src/components/TrustBadge.jsx` (NEW)
- `extension/src/components/ResultsView.jsx` (NEW)
- `extension/src/components/Popup.jsx` (UPDATED - now uses ResultsView)

Extension rebuilt: **272KB** (gzipped: 88KB)

---

## Quick Reload

After making changes:
1. `cd extension && npm run build`
2. Click refresh on extension in chrome://extensions/
3. Close and reopen popup
4. Test again

---

Ready to test! Click that icon and see it in action. 🎨
