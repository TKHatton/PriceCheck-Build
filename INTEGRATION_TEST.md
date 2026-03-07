# End-to-End Integration Test

## Status: Ready to Test

Both backend and extension are wired together. Follow these steps to verify the full pipeline.

## Prerequisites

1. **Backend server running:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Extension loaded in Chrome:**
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select `extension/dist/` folder

## Test Flow

### What Happens When You Click "Analyze This Page"

1. **Extension popup** sends message to content script:
   ```javascript
   chrome.tabs.sendMessage(tabId, { action: 'extractPageData' })
   ```

2. **Content script** extracts page data:
   - `url` - Current page URL
   - `title` - Document title
   - `bodyText` - Page content (up to 15k chars)
   - `priceElements` - Extracted price patterns

3. **Popup** POSTs to backend:
   ```
   POST http://localhost:8000/analyze
   {
     "input_type": "page",
     "page_url": "...",
     "page_title": "...",
     "body_text": "...",
     "price_elements": [...]
   }
   ```

4. **Backend pipeline** executes:
   ```
   input_router → content_node → trust_node → trust_gate
                                                    ↓
   (if trust ≥ 30)                      analyze_node → score_node → output_node
   (if trust < 30)                      output_node (scam exit)
   ```

5. **Response** returned to popup:
   ```json
   {
     "gaslighting_score": 24,
     "severity_label": "Mildly Misleading",
     "tactics": [...],
     "trust_score": 100,
     "is_scam": false,
     ...
   }
   ```

6. **Popup displays** result and logs to console

## Test Scenarios

### Scenario 1: Manipulative Product Page

**Test Site:** Create a simple HTML file or use a test page:

```html
<!DOCTYPE html>
<html>
<head><title>Amazing Deal!</title></head>
<body>
  <h1>Limited Time Offer!</h1>
  <p>WAS $299 NOW ONLY $79!</p>
  <p>SALE ENDS IN 09:47!</p>
  <p>Only 3 left in stock!</p>
  <p>Free trial - $49/month after</p>
</body>
</html>
```

**Expected Console Output:**
```
[Popup] Page data extracted: {url, title, bodyText, priceElements}
[Popup] Full analysis result: {...}
[Popup] Gaslighting score: 20-30
[Popup] Severity label: "Mildly Misleading"
[Popup] Tactics found: 3
[Popup] Trust score: 100
[Popup] Is scam: false
```

**Expected in Popup UI:**
- Shows "Analysis Result" box
- Score: 20-30
- Label: Mildly Misleading
- Tactics: 3
- Trust: 100

### Scenario 2: Clean Product Page

**Test Content:**
```html
<!DOCTYPE html>
<html>
<head><title>Quality Product</title></head>
<body>
  <h1>Premium Running Shoes</h1>
  <p>Price: $120</p>
  <p>Fast shipping available</p>
</body>
</html>
```

**Expected:**
- Score: 0-5
- Label: "Honest Pricing"
- Tactics: 0-1
- Trust: 100

### Scenario 3: Scam Site (Fake Brand)

**Test Content:**
```html
<!DOCTYPE html>
<html>
<head><title>Nike Official - 95% OFF</title></head>
<body>
  <h1>Nike Outlet Sale</h1>
  <p>Everything 95% off!</p>
  <p>Contact: sales@gmail.com</p>
</body>
</html>
```

**Expected:**
- Trust score: <30
- Is scam: true
- Score: 95
- Label: "Fraudulent Storefront"
- Shows "⚠️ SCAM DETECTED"

## Debugging

### Check Backend Logs

Watch terminal running uvicorn for node execution:
```
[input_router] Processing input_type: page
[content_node] Processing page: https://...
[trust_node] Checking trust for: https://...
[trust_node] Trust score: 100, Signals: 1
[trust_gate] Trust passed - routing to analyze
[analyze_node] Analyzing with Claude API
[claude] Analysis complete: 3 tactics found
[score_node] Calculating gaslighting score
[score_node] Final score: 24 (Mildly Misleading)
[output_node] Preparing final output
```

### Check Extension Console

1. Open popup
2. Right-click in popup → "Inspect"
3. Check Console tab for logs:
   - `[Popup] Page data extracted:`
   - `[Popup] Full analysis result:`

### Check Content Script Console

1. Navigate to test page
2. Open DevTools (F12)
3. Check Console for:
   - `PriceCheck content script loaded`

## Common Issues

### Error: "No active tab found"
- Ensure you're on a valid webpage (not chrome:// or extension pages)
- Try refreshing the page

### Error: "API error: 404"
- Backend server not running
- Start with: `cd backend && python -m uvicorn app.main:app --reload --port 8000`

### Error: "Content script error"
- Extension not loaded or needs refresh
- Reload extension in chrome://extensions/
- Refresh the test page

### CORS Error
- Backend CORS allows `chrome-extension://*`
- Check backend logs for CORS-related errors

### No tactics detected (ANTHROPIC_API_KEY)
- Ensure .env has valid ANTHROPIC_API_KEY
- Check backend logs: `[claude] ANTHROPIC_API_KEY not set`

## Score Verification

The scoring algorithm applies these weights:

| Category | Weight | Example Severity | Weighted Score |
|----------|--------|------------------|----------------|
| FAKE_DISCOUNT | 1.2 | 8 | 9.6 |
| DARK_PATTERNS | 0.9 | 9 | 8.1 |
| SUBSCRIPTION_TRAP | 1.1 | 6 | 6.6 |
| **Total** | | | **24.3 → 24** |

Labels:
- 0-20: Honest Pricing
- 21-45: Mildly Misleading
- 46-70: Actively Deceptive
- 71-100: Full Gaslighting

## Next Steps

Once end-to-end testing passes:
1. Implement ResultsView component (replace debug display)
2. Add loading narrative animation
3. Add trust badge UI
4. Implement tactic cards with reveal animation
5. Add split-screen price comparison
