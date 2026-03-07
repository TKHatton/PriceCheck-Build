# PriceCheck - Local Testing Guide

## Current Status: ✓ Backend Running, Extension Ready

The backend server is running on `http://localhost:8000` and the extension is built and ready to load.

---

## Step 1: Verify Backend is Running

The backend is already started. Test it:

1. Open your browser and go to: `http://localhost:8000/health`
2. You should see: `{"status":"ok"}`

If you see this, **backend is working!** ✓

If not, run this in a terminal:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Step 2: Load Extension in Chrome

1. **Open Chrome** and navigate to: `chrome://extensions/`

2. **Enable Developer mode:**
   - Look for toggle switch in top-right corner
   - Click to enable it

3. **Load the extension:**
   - Click "Load unpacked" button
   - Navigate to: `C:\Users\ltken\OneDrive\Documents\GitHub\PriceCheck-Build\extension\dist`
   - Select the `dist` folder and click "Select Folder"

4. **Verify extension loaded:**
   - You should see "PriceCheck" card appear
   - Red square icon (placeholder) should appear in your toolbar
   - If you don't see the icon, click the puzzle piece icon in toolbar and pin PriceCheck

---

## Step 3: Test with the Test Page

1. **Open the test page:**
   - Double-click: `C:\Users\ltken\OneDrive\Documents\GitHub\PriceCheck-Build\test-page.html`
   - Or drag it into Chrome

2. **Open DevTools (IMPORTANT for debugging):**
   - Press `F12` or right-click page → "Inspect"
   - Click "Console" tab
   - You should see: `PriceCheck content script loaded`
   - If you don't see this, the content script isn't running

3. **Click the PriceCheck extension icon** (red square in toolbar)
   - A popup should open with:
     - "PriceCheck" title in red
     - "See the real price. Stop getting played."
     - Red "Analyze This Page" button

4. **Click "Analyze This Page" button:**
   - Button text changes to "Analyzing..."
   - Watch the Console tab for logs

5. **Check Console for logs:**
   You should see:
   ```
   [Popup] Page data extracted: {...}
   [Popup] Full analysis result: {...}
   [Popup] Gaslighting score: 24
   [Popup] Severity label: "Mildly Misleading"
   [Popup] Tactics found: 3
   [Popup] Trust score: 100
   [Popup] Is scam: false
   ```

6. **Check the popup:**
   - "Analysis Result" box should appear
   - Score: 20-30
   - Label: Mildly Misleading
   - Tactics: 3
   - Trust: 100

---

## Step 4: Test on a Real Website (Optional)

Try it on a real e-commerce site like Amazon:

1. Navigate to any Amazon product page
2. Click PriceCheck icon
3. Click "Analyze This Page"
4. Check console and popup for results

---

## Troubleshooting

### Problem: "PriceCheck content script loaded" doesn't appear in console

**Solution:**
1. Go to `chrome://extensions/`
2. Find PriceCheck
3. Click the refresh icon (circular arrow) on the PriceCheck card
4. Refresh the test page (F5)
5. Check console again

### Problem: Popup shows error "No active tab found"

**Solution:**
- Make sure you're on a normal webpage (not chrome:// pages)
- Try refreshing the page

### Problem: Popup shows error "API error: 404" or "Failed to fetch"

**Solution:**
- Backend server may have stopped
- Check if `http://localhost:8000/health` works in browser
- If not, restart backend:
  ```bash
  cd backend
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

### Problem: Popup doesn't open when clicking icon

**Solution:**
1. Check for errors in extension:
   - Go to `chrome://extensions/`
   - Find PriceCheck
   - Click "Errors" button if it's red
2. Rebuild extension:
   ```bash
   cd extension
   npm run build
   ```
3. Click refresh icon on extension card
4. Try again

### Problem: Console shows "chrome.tabs is not defined" or similar

**Solution:**
- You might be inspecting the wrong console
- Make sure you're looking at the webpage console (F12 on the page), NOT the popup console
- For popup console: right-click inside popup → "Inspect" → check Console there

### Problem: No logs appear in console at all

**Solution:**
1. Open the popup
2. Right-click INSIDE the popup → "Inspect"
3. This opens the popup's DevTools
4. Check Console tab there for popup-specific logs

---

## Expected Results on Test Page

The test page has:
- **Fake discount:** "WAS $299 NOW $79"
- **Countdown timer:** "SALE ENDS IN 09:47"
- **False scarcity:** "Only 3 left"
- **Subscription trap:** "Free trial - $49/month after"

**Expected Analysis:**
- **Gaslighting Score:** 20-30
- **Label:** "Mildly Misleading"
- **Tactics:** 3-4
  1. FAKE_DISCOUNT (severity 8)
  2. DARK_PATTERNS (severity 9)
  3. SUBSCRIPTION_TRAP (severity 6)
- **Trust Score:** 100
- **Is Scam:** false

---

## Quick Command Reference

**Start backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Rebuild extension:**
```bash
cd extension
npm run build
```

**Test backend directly:**
```bash
curl http://localhost:8000/health
```

**Check if server is running:**
```bash
netstat -ano | findstr :8000
```

---

## What You Should See

### When Everything Works:

1. **Backend terminal shows:**
   ```
   INFO: Uvicorn running on http://0.0.0.0:8000
   INFO: Started reloader process
   ```

2. **Extension loads without errors in chrome://extensions/**

3. **Test page console shows:**
   ```
   PriceCheck content script loaded
   ```

4. **After clicking "Analyze This Page":**
   - Popup shows "Analyzing..." briefly
   - Console shows detailed logs
   - Popup shows results box with score and tactics
   - No error messages

5. **Backend terminal shows:**
   ```
   [input_router] Processing input_type: page
   [content_node] Processing page: ...
   [trust_node] Checking trust for: ...
   [analyze_node] Analyzing with Claude API
   [score_node] Calculating gaslighting score
   [output_node] Preparing final output
   INFO: 127.0.0.1:... - "POST /analyze HTTP/1.1" 200 OK
   ```

---

## Need Help?

If you're still stuck, check:
1. Backend logs in terminal (errors will appear there)
2. Browser console (F12 on webpage)
3. Popup console (right-click in popup → Inspect)
4. Extension errors (chrome://extensions/ → Errors button)

The most common issue is the backend not running or the extension not loaded properly.
