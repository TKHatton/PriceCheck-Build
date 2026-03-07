# PriceCheck Deployment Guide

## Architecture Overview

- **Backend:** FastAPI on Render (render.yaml)
- **Extension:** Chrome Web Store
- **Landing:** Netlify

---

## Backend Deployment (Render)

### Option 1: Using render.yaml (Recommended)

1. **Push code to GitHub**

2. **Create new Web Service on Render:**
   - Connect your GitHub repository
   - Render auto-detects `backend/render.yaml`
   - Or manually set:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set environment variables in Render dashboard:**
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-...
   WHOIS_API_KEY=your_whois_key (optional)
   URLSCAN_API_KEY=your_urlscan_key (optional)
   CLAUDE_MODEL=claude-3-haiku-20240307 (optional, has default)
   FRONTEND_URL= (optional, leave blank for default CORS)
   ```

4. **Deploy**
   - Render auto-deploys on git push
   - Get your API URL: `https://pricecheck-api.onrender.com`

### Option 2: Using Dockerfile

If you prefer Docker deployment or different hosting:

```bash
cd backend
docker build -t pricecheck-api .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  pricecheck-api
```

---

## Landing Page Deployment (Netlify)

### Setup

1. **Build the landing page:**
   ```bash
   cd landing
   npm install
   npm run build
   ```

2. **Deploy to Netlify:**

   **Option A: Netlify CLI**
   ```bash
   npm install -g netlify-cli
   netlify deploy --dir=dist --prod
   ```

   **Option B: Drag and Drop**
   - Go to https://app.netlify.com/drop
   - Drag the `landing/dist` folder
   - Get your URL: `https://your-site.netlify.app`

   **Option C: Git Integration**
   - Connect GitHub repo to Netlify
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Base directory: `landing`

### Configuration

No environment variables needed for landing page. It's a static site.

---

## Chrome Extension Publishing

### Prepare Extension

1. **Update manifest.json:**
   - Remove test/placeholder content
   - Add real icons (replace 1x1 red pixels)
   - Update description if needed

2. **Update backend URL in extension:**

   In `extension/src/components/Popup.jsx`, change:
   ```javascript
   // FROM:
   const response = await fetch('http://localhost:8000/analyze', {

   // TO:
   const response = await fetch('https://pricecheck-api.onrender.com/analyze', {
   ```

   Or make it configurable:
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   const response = await fetch(`${API_URL}/analyze`, {
   ```

3. **Build production extension:**
   ```bash
   cd extension
   npm run build
   ```

4. **Create zip for Chrome Web Store:**
   ```bash
   cd extension/dist
   zip -r ../pricecheck-extension.zip *
   ```

   Or on Windows:
   - Select all files in `extension/dist`
   - Right-click → Send to → Compressed folder
   - Name it `pricecheck-extension.zip`

### Submit to Chrome Web Store

1. Go to: https://chrome.google.com/webstore/devconsole
2. Pay $5 developer fee (one-time)
3. Click "New Item"
4. Upload `pricecheck-extension.zip`
5. Fill in store listing:
   - Name: PriceCheck
   - Description: See the real price. Stop getting played.
   - Category: Shopping
   - Screenshots: (capture extension in action)
   - Privacy policy URL: (required - can host on Netlify)
6. Submit for review (1-3 days)

---

## Environment Variables Summary

### Backend (Render)

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `ANTHROPIC_API_KEY` | Yes | - | Claude API access |
| `WHOIS_API_KEY` | No | - | Domain age checking |
| `URLSCAN_API_KEY` | No | - | Domain trust checks |
| `CLAUDE_MODEL` | No | claude-3-haiku-20240307 | Model selection |
| `FRONTEND_URL` | No | - | Custom CORS origin |
| `PORT` | Auto-set | 8000 | Render sets this |

### Extension

No backend env vars needed in extension build. The API URL can be:
- Hardcoded: `https://pricecheck-api.onrender.com`
- Or configured via Vite env: `VITE_API_URL`

### Landing

No env vars needed. It's a static site.

---

## CORS Configuration

Backend allows requests from:
- `chrome-extension://*` (any extension origin)
- `https://*.netlify.app` (Netlify deployments)
- `http://localhost:5173` (local dev)
- `http://localhost:3000` (alternative dev)
- Custom `FRONTEND_URL` if set

---

## Post-Deployment Checklist

### Backend
- [ ] Health endpoint works: `https://your-app.onrender.com/health`
- [ ] Returns: `{"status": "ok"}`
- [ ] Environment variables set in Render dashboard
- [ ] ANTHROPIC_API_KEY is valid

### Landing
- [ ] Site loads: `https://your-site.netlify.app`
- [ ] All 6 sections visible
- [ ] CTAs link correctly
- [ ] Responsive on mobile (test at 375px)

### Extension
- [ ] Built with production API URL
- [ ] Tested locally with production backend
- [ ] Icons replaced with real icons (not red pixels)
- [ ] Zip file created
- [ ] Ready for Chrome Web Store submission

---

## Testing Production Setup Locally

Before deploying, test production-like setup:

**1. Backend with production CORS:**
```bash
cd backend
# .env already has ANTHROPIC_API_KEY
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**2. Landing page:**
```bash
cd landing
npm run build
npm run preview
# Opens at http://localhost:4173
```

**3. Extension:**
```bash
cd extension
npm run build
# Load extension/dist in Chrome
```

---

## Monitoring

### Backend Logs (Render)
- View in Render dashboard → Logs tab
- See all LangGraph node execution
- Monitor API errors

### Extension Errors
- Users can see errors in extension popup
- No analytics built in yet

### Landing Analytics
- Can add Google Analytics or Plausible
- Track Install button clicks

---

## Costs

- **Render Free Tier:** $0 (spins down after inactivity, cold starts)
- **Render Starter:** $7/month (always on, no cold starts)
- **Netlify:** $0 for static sites
- **Chrome Web Store:** $5 one-time developer fee
- **Anthropic API:** Pay per use (Haiku is cheap, ~$0.25 per 1M tokens)

---

## Files Created

- `backend/render.yaml` - Render deployment config
- `backend/Dockerfile` - Docker fallback
- `backend/.dockerignore` - Docker build exclusions
- `backend/app/main.py` - Updated CORS
- `backend/.env.example` - Updated with FRONTEND_URL docs
- `DEPLOYMENT.md` - This guide

---

Ready to deploy! Start with backend to Render, then landing to Netlify. 🚀
