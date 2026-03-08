import React, { useState } from 'react';
import LoadingNarrative from './LoadingNarrative';
import ResultsView from './ResultsView';

function Popup() {
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [pageTitle, setPageTitle] = useState('');

  const loadingSteps = [
    'Reading this page...',
    'Checking domain trust...',
    'Analyzing pricing tactics...',
    'Calculating your Gaslighting Score...'
  ];

  const handleAnalyze = async () => {
    setAnalyzing(true);
    setError(null);
    setResult(null);
    setPageTitle('');

    try {
      // Step 1: Get active tab info
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      if (!tab?.id) {
        throw new Error('No active tab found');
      }

      // Store page title for display
      setPageTitle(tab.title || 'Product Page');

      // Step 2: Capture screenshot as base64 PNG
      const screenshotDataUrl = await chrome.tabs.captureVisibleTab(null, { format: 'png' });

      // Extract base64 string (remove "data:image/png;base64," prefix)
      const base64Image = screenshotDataUrl.split(',')[1];

      console.log('[Popup] Screenshot captured:', base64Image.length, 'characters');

      // Build request payload for OCR/Vision analysis
      const requestPayload = {
        input_type: 'image',
        page_url: tab.url || '',
        page_title: tab.title || '',
        body_text: '',
        price_elements: [],
        raw_image_b64: base64Image
      };

      // Step 3: POST to backend API
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestPayload)
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      // Step 4: Parse and log response
      const analysisResult = await response.json();

      console.log('[Popup] Full analysis result:', analysisResult);
      console.log('[Popup] Gaslighting score:', analysisResult.gaslighting_score);
      console.log('[Popup] Severity label:', analysisResult.severity_label);
      console.log('[Popup] Tactics found:', analysisResult.tactics?.length || 0);
      console.log('[Popup] Trust score:', analysisResult.trust_score);
      console.log('[Popup] Is scam:', analysisResult.is_scam);

      // DEBUG: Send to debug endpoint after analysis
      try {
        const debugResponse = await fetch('http://localhost:8000/debug-input', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestPayload)
        });
        const debugData = await debugResponse.json();
        console.log('PRICECHECK DEBUG:', debugData);
      } catch (debugErr) {
        console.error('Debug endpoint failed:', debugErr);
      }

      setResult(analysisResult);

    } catch (err) {
      console.error('[Popup] Analysis failed:', err);
      setError(err.message || 'Analysis failed. Please try again.');
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

      {/* Loading Narrative */}
      {analyzing && (
        <div className="mt-6">
          <LoadingNarrative steps={loadingSteps} />
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-4 bg-red-tint border border-red-mid rounded">
          <p className="font-body text-sm text-red-alarm">
            <strong>Error:</strong> {error}
          </p>
        </div>
      )}

      {/* Results: Always show ResultsView (trust gate disabled) */}
      {result && !analyzing && (
        <ResultsView result={result} pageTitle={pageTitle} />
      )}
    </div>
  );
}

export default Popup;
