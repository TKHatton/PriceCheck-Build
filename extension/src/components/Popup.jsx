import React, { useState } from 'react';

function Popup() {
  const [analyzing, setAnalyzing] = useState(false);

  const handleAnalyze = async () => {
    setAnalyzing(true);

    try {
      // Get active tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      // Send message to content script to extract page data
      const pageData = await chrome.tabs.sendMessage(tab.id, { action: 'extractPageData' });

      console.log('Page data extracted:', pageData);

      // TODO: Send to backend API
      // const response = await fetch('http://localhost:8000/analyze', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     input_type: 'page',
      //     ...pageData,
      //     price_elements: pageData.priceElements || []
      //   })
      // });
      // const result = await response.json();
      // console.log('Analysis result:', result);

    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="w-[400px] min-h-[200px] bg-paper p-6">
      <h1 className="font-display text-4xl font-bold text-red-alarm mb-2">
        PriceCheck
      </h1>

      <p className="font-body text-ink-mid text-sm mb-6">
        See the real price. Stop getting played.
      </p>

      <button
        onClick={handleAnalyze}
        disabled={analyzing}
        className="w-full bg-red-alarm text-white font-display text-lg font-bold py-3 px-6 rounded hover:bg-red-600 transition-colors duration-hover disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {analyzing ? 'Analyzing...' : 'Analyze This Page'}
      </button>
    </div>
  );
}

export default Popup;
