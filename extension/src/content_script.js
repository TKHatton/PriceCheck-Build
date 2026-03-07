// Content script runs in the context of web pages
// Has access to the DOM but not to Chrome extension APIs directly

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action !== 'extractPageData') return;

  try {
    // Extract page data
    const data = {
      url: window.location.href,
      title: document.title,
      bodyText: document.body.innerText.slice(0, 15000),
      priceElements: extractPriceElements(),
      metaDescription: getMeta('description'),
    };

    sendResponse(data);
  } catch (error) {
    console.error('Error extracting page data:', error);
    sendResponse({ error: error.message });
  }

  // Return true to indicate we will send a response asynchronously
  return true;
});

function extractPriceElements() {
  // Find elements containing price patterns
  // Looks for: $ symbols, was/now patterns, % off, countdown timers
  const priceElements = [];
  const pricePatterns = /\$[\d,]+\.?\d*|was|now|\d+%\s*off/gi;

  // Search through common price-containing elements
  const selectors = [
    '[class*="price"]',
    '[id*="price"]',
    '[class*="cost"]',
    '[class*="discount"]',
    '[class*="sale"]',
    'span',
    'div'
  ];

  document.querySelectorAll(selectors.join(',')).forEach(el => {
    const text = el.textContent.trim();
    if (text && pricePatterns.test(text) && text.length < 200) {
      priceElements.push({
        text: text,
        selector: getSelector(el)
      });
    }
  });

  // Limit to first 20 price elements to avoid overwhelming the API
  return priceElements.slice(0, 20);
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
