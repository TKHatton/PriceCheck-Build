# PriceCheck - Complete UI Test Guide

## ✓ All Components Built - Ready to Test

Extension rebuilt with complete UI including scam detection view.

---

## Components Summary

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **LoadingNarrative** | Loading animation | 4 steps, 700ms stagger |
| **TrustBadge** | Trust indicator | 3 states: PASS (fades), WARN (persists), FAIL (hidden) |
| **ScamView** | Fraud warning | Red warning, lists fraud signals, no score |
| **ResultsView** | Normal results | Trust badge, split screen, tactics, score |
| **SplitScreen** | Price comparison | What they show vs what's happening |
| **TacticCard** | Tactic display | Severity-coded colors and borders |
| **ScoreDisplay** | Gaslighting score | Count-up animation, dynamic colors |

---

## Test Scenarios

### Scenario 1: Normal Product Page (PASS)

**File:** `test-page.html`

**What to watch for:**
1. **Loading:** 4 steps appear sequentially
2. **Trust Badge:** Green pill "Verified Retailer" appears, then fades out after 2s
3. **Split Screen:**
   - Top: "WHAT THEY SHOW" - white box
   - Bottom: "WHAT IS REALLY HAPPENING" - light red box
4. **Tactic Cards:** 3 cards slide in one by one:
   - FAKE DISCOUNT (red border)
   - DARK PATTERNS (red border)
   - SUBSCRIPTION TRAP (amber border)
5. **Score:** Counts up 0 → 24, color is **amber** (21-45 range)
6. **Label:** "MILDLY MISLEADING"

**Timeline:**
- 0s: Click button
- 0-2.5s: Loading narrative
- 3s: Results appear
- 3s: Green trust badge shows
- 5s: Trust badge fades out
- 3-4.4s: Score counts up

---

### Scenario 2: Scam Site (FAIL)

**File:** `test-scam-page.html`

**What to watch for:**
1. **Loading:** Same 4 steps
2. **NO ResultsView shown**
3. **ScamView appears:**
   - White background with 4px red border
   - 🚨 emoji at top
   - Heading: "THIS SITE RAISED FRAUD SIGNALS"
   - Subhead: "We recommend not entering payment information..."
   - Section "RED FLAGS DETECTED:"
   - 3 bullet points (fade in sequentially):
     * Page claims to be Nike but domain doesn't match
     * Prices appear implausibly low (95% off)
     * Business contact uses Gmail
   - Disclaimer at bottom
4. **NO gaslighting score shown**
5. **NO tactic cards shown**

**Timeline:**
- 0s: Click button
- 0-2.5s: Loading narrative
- 3s: ScamView appears (not normal results)

---

### Scenario 3: Suspicious But Not Scam (WARN)

To test this, you'd need a page with:
- Trust score 30-69
- Example: Implausible pricing but legitimate domain

**Expected:**
- Amber trust badge: "Could not fully verify this retailer"
- Badge PERSISTS (does not fade out)
- Normal ResultsView below badge
- Tactic cards and score display normally

---

## Visual Checklist

### Loading State
- [ ] 4 lines appear sequentially
- [ ] JetBrains Mono font (monospace)
- [ ] Smooth fade-in animations
- [ ] Timing feels natural (not too fast/slow)

### TrustBadge - PASS State
- [ ] Green rounded pill
- [ ] "Verified Retailer" text
- [ ] Appears at top
- [ ] Fades out after 2 seconds
- [ ] Smooth exit animation

### TrustBadge - WARN State
- [ ] Amber box with warning icon ⚠️
- [ ] "Could not fully verify this retailer"
- [ ] Stays visible (doesn't fade)
- [ ] Clear but not alarming

### ScamView (is_scam = true)
- [ ] Large red warning
- [ ] 🚨 emoji visible
- [ ] Clear heading in red
- [ ] Red flags listed with bullets
- [ ] Easy to read (not overwhelming)
- [ ] Disclaimer at bottom
- [ ] NO score display
- [ ] Professional but serious tone

### SplitScreen
- [ ] Two sections stacked (not side-by-side)
- [ ] "WHAT THEY SHOW" label in caps
- [ ] "WHAT IS REALLY HAPPENING" label in caps
- [ ] Red-tint background on bottom section
- [ ] Prices formatted with $ and decimals
- [ ] Delta shown if present

### TacticCard
- [ ] Red cards for high severity (7+)
- [ ] Amber cards for medium (4-6)
- [ ] White/gray for low (<4)
- [ ] Name in uppercase, bold
- [ ] Evidence in quotes, italic, monospace
- [ ] Explanation readable
- [ ] Cards appear with stagger (80ms)

### ScoreDisplay
- [ ] Large number (6xl size)
- [ ] Counts up smoothly from 0
- [ ] Takes 1.2 seconds
- [ ] Color changes: green (0-20), amber (21-45), red (46+)
- [ ] Red border and box shadow
- [ ] /100 in lighter gray
- [ ] Severity label below in caps
- [ ] Centered in popup

---

## Color Accuracy

| Element | Expected Color | Hex |
|---------|---------------|-----|
| Red borders | Bright red | #D42B2B |
| Red backgrounds | Very light pink | #FDF1F1 |
| Amber borders | Orange | #C47C00 |
| Amber backgrounds | Light yellow | #FDF6E8 |
| Green (trust) | Forest green | #1A7A4A |
| Green background | Light mint | #EDF7F2 |
| Page background | Warm off-white | #FAF9F6 |

---

## Font Accuracy

| Text | Expected Font | Notes |
|------|--------------|-------|
| "PriceCheck" title | Barlow Condensed | Bold, condensed sans |
| Score number | Barlow Condensed | Very bold, large |
| Tactic names | Barlow Condensed | Bold, uppercase |
| Loading steps | JetBrains Mono | Monospace |
| Evidence quotes | JetBrains Mono | Monospace, italic |
| Labels (WHAT THEY SHOW) | JetBrains Mono | Monospace, small, uppercase |
| Body text | Libre Franklin | Clean sans-serif |

---

## How to Test All Views

### Test Normal Results:
1. Open `test-page.html`
2. Click PriceCheck icon
3. Click "Analyze This Page"
4. Watch for: Loading → Trust Badge (fades) → Results → Score

### Test Scam Warning:
1. Open `test-scam-page.html`
2. Click PriceCheck icon
3. Click "Analyze This Page"
4. Watch for: Loading → ScamView (red warning, no score)

### Test on Real Sites:
- Amazon product page (should be clean or mildly misleading)
- Any sketchy-looking deal site (might trigger warnings)

---

## Reload Extension After Build

**Every time you rebuild:**
1. Go to `chrome://extensions/`
2. Find PriceCheck
3. Click refresh icon (circular arrow)
4. Close popup if open
5. Test again

---

## Console Commands for Debugging

**Check if server is running:**
```bash
curl http://localhost:8000/health
```

**Restart backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Rebuild extension:**
```bash
cd extension
npm run build
```

---

## What to Give Feedback On

As you test, think about:

1. **Animation timing:** Too fast? Too slow? Just right?
2. **Color severity coding:** Clear which is bad vs good?
3. **Text sizes:** Anything too small/large?
4. **Spacing:** Cramped or comfortable?
5. **Score emphasis:** Is it the hero of the design?
6. **Scam warning:** Clear and serious without being scary?
7. **Overall polish:** Does it feel like a real product?

---

## Expected Behavior Summary

| Page Type | Trust Score | View Shown | Score Shown | Badge State |
|-----------|-------------|------------|-------------|-------------|
| Clean site | 100 | ResultsView | Yes, 0-20 | Green, fades |
| Suspicious | 80 | ResultsView | Yes, varies | Green, fades |
| Questionable | 50 | ResultsView | Yes, varies | Amber, persists |
| Scam | 15 | ScamView | NO | Not shown |

---

Ready to test! Open the test pages and see the complete UI in action. 🎨
