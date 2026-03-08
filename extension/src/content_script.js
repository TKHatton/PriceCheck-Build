// Content script runs in the context of web pages
// Has access to the DOM but not to Chrome extension APIs directly

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action !== 'extractPageData') return;

  // Wait 1500ms for React-rendered content to load (Temu needs more time)
  setTimeout(() => {
    try {
      // Extract page data
      const data = {
        url: window.location.href,
        title: document.title,
        bodyText: getBodyText(),
        priceElements: extractPriceElements(),
        metaDescription: getMeta('description'),
      };

      sendResponse(data);
    } catch (error) {
      console.error('Error extracting page data:', error);
      sendResponse({ error: error.message });
    }
  }, 1500);

  // Return true to keep message channel open for async response
  return true;
});

function extractPriceElements() {
  // Fix 2: Comprehensive price element extraction
  const priceElements = [];
  const seenTexts = new Set(); // For deduplication

  // Price and manipulation patterns
  const pricePatterns = [
    /\$[\d,]+\.?\d*/,                    // Dollar amounts
    /\d+%\s*off/i,                       // Percent off
    /\bwas\b|\bnow\b/i,                  // Was/now language
    /only\s+\d+\s+left/i,                // "only X left"
    /selling\s+fast/i,                   // "selling fast"
    /limited\s+time/i,                   // "limited time"
    /ends?\s+in/i,                       // "ends in"
    /best[-\s]sell/i,                    // "best-seller"
    /\d+k?\+?\s*sold/i                   // "X sold", "Xk+ sold"
  ];

  // Query all relevant text-containing elements
  const textElements = document.querySelectorAll('span, div, p, strong, b, h1, h2, h3');

  textElements.forEach(el => {
    // Skip elements with many children (likely containers)
    if (el.children.length >= 4) return;

    const text = el.innerText?.trim();
    if (!text || text.length > 200) return;

    // Check if text matches any price pattern
    const matches = pricePatterns.some(pattern => pattern.test(text));
    if (matches && !seenTexts.has(text)) {
      seenTexts.add(text);
      priceElements.push({
        text: text,
        selector: getSelector(el)
      });
    }
  });

  // Also capture strikethrough elements (crossed-out prices)
  document.querySelectorAll('del, s').forEach(el => {
    const text = el.innerText?.trim();
    if (text && text.length < 200 && !seenTexts.has(text)) {
      seenTexts.add(text);
      priceElements.push({
        text: text,
        selector: getSelector(el)
      });
    }
  });

  // Query elements with price-related attributes
  const attributeSelectors = [
    '[data-price]',
    '[data-original-price]',
    '[data-sale-price]',
    '[aria-label*="price" i]',
    '[aria-label*="$" i]',
    '[aria-label*="off" i]'
  ];

  document.querySelectorAll(attributeSelectors.join(',')).forEach(el => {
    // Get text from element or aria-label
    const text = el.innerText?.trim() || el.getAttribute('aria-label')?.trim();
    if (text && text.length < 200 && !seenTexts.has(text)) {
      seenTexts.add(text);
      priceElements.push({
        text: text,
        selector: getSelector(el)
      });
    }

    // Also capture data-price attribute values
    const dataPrice = el.getAttribute('data-price') ||
                      el.getAttribute('data-original-price') ||
                      el.getAttribute('data-sale-price');
    if (dataPrice && !seenTexts.has(dataPrice)) {
      seenTexts.add(dataPrice);
      priceElements.push({
        text: dataPrice,
        selector: getSelector(el)
      });
    }
  });

  // Brute force pass: scan ALL elements for anything we might have missed
  document.querySelectorAll('*').forEach(el => {
    const text = el.innerText?.trim();
    if (!text || text.length >= 50 || seenTexts.has(text)) return;

    // Check for price patterns
    if (/\$[\d]/.test(text) || /\d+%/.test(text) || /off/i.test(text) || /sold/i.test(text)) {
      seenTexts.add(text);
      priceElements.push({
        text: text,
        selector: getSelector(el)
      });
    }
  });

  // Return up to 50 results
  return priceElements.slice(0, 50);
}

function getBodyText() {
  // Fix 3: Clean body text extraction with additional price data
  const bodyClone = document.body.cloneNode(true);

  // Remove script, style, noscript elements from clone
  bodyClone.querySelectorAll('script, style, noscript').forEach(el => el.remove());

  // Get cleaned text content (limit to 15000 chars)
  let bodyText = bodyClone.innerText.slice(0, 15000);

  // Append additional price data from attributes
  const additionalData = [];

  // Collect aria-label values
  document.querySelectorAll('[aria-label]').forEach(el => {
    const label = el.getAttribute('aria-label');
    if (label && (label.includes('$') || label.toLowerCase().includes('price') || label.toLowerCase().includes('off'))) {
      additionalData.push(label);
    }
  });

  // Collect data-price attributes
  document.querySelectorAll('[data-price], [data-original-price], [data-sale-price]').forEach(el => {
    const price = el.getAttribute('data-price') ||
                  el.getAttribute('data-original-price') ||
                  el.getAttribute('data-sale-price');
    if (price) {
      additionalData.push(price);
    }
  });

  // Append additional data section if any found
  if (additionalData.length > 0) {
    const uniqueData = [...new Set(additionalData)]; // Deduplicate
    bodyText += '\n\n[ADDITIONAL PRICE DATA]\n' + uniqueData.slice(0, 20).join('\n');
  }

  return bodyText;
}

function getMeta(name) {
  const el = document.querySelector(`meta[name='${name}']`);
  return el ? el.getAttribute('content') : '';
}

function getSelector(el) {
  // Generate a simple selector for the element
  if (el.id) return `#${el.id}`;
  if (el.className) {
    const classes = Array.from(el.classList).slice(0, 2).join('.');
    return `.${classes}`;
  }
  return el.tagName.toLowerCase();
}

console.log('PriceCheck content script loaded');
