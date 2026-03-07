# PriceCheck Chrome Extension

Chrome extension that exposes pricing manipulation tactics used by retailers.

## Development Setup

1. Install dependencies:
```bash
npm install
```

2. Build the extension:
```bash
npm run build
```

3. Load in Chrome:
   - Open `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `dist/` folder

## Development Mode

For live development with hot reload:
```bash
npm run dev
```

Then load the `dist/` folder as an unpacked extension in Chrome.

## Project Structure

```
extension/
├── public/
│   ├── manifest.json        # Chrome extension manifest v3
│   └── icon*.png           # Extension icons (placeholders)
├── src/
│   ├── components/
│   │   └── Popup.jsx       # Main popup component
│   ├── content_script.js   # Injected into web pages
│   ├── popup.html          # Popup entry point
│   ├── popup.jsx           # React root
│   └── index.css           # Tailwind CSS
├── vite.config.js          # Vite build configuration
├── tailwind.config.js      # Design tokens
└── package.json
```

## How It Works

1. User clicks the PriceCheck icon on any product page
2. Popup opens with "Analyze This Page" button
3. Content script extracts page data (URL, title, text, prices)
4. Data is sent to backend API for analysis
5. Results display in the popup with gaslighting score and tactics

## Design System

All colors, fonts, and motion tokens are defined in `tailwind.config.js`:
- Colors: red-alarm, paper, ink, trust, amber variants
- Fonts: Barlow Condensed (display), Libre Franklin (body), JetBrains Mono (mono)
- 400px fixed width for popup

## Next Steps

- [ ] Add ResultsView component
- [ ] Add loading state with narrative sequence
- [ ] Connect to backend API
- [ ] Add error handling
- [ ] Implement result animations
