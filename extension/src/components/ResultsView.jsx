import React from 'react';
import SplitScreen from './SplitScreen';
import ScoreDisplay from './ScoreDisplay';

function ResultsView({ result, pageTitle }) {
  if (!result) return null;

  return (
    <div className="mt-6 space-y-6">
      {/* Trust Badge removed - trust gate disabled */}

      {/* Split Screen: Price Comparison and Tactic Cards */}
      <SplitScreen
        pageTitle={pageTitle || result.page_title || 'Product Page'}
        marketedPrice={result.marketed_price}
        realPrice={result.real_price}
        priceDelta={result.price_delta}
        realCostNote={result.real_cost_note}
        tactics={result.tactics || []}
      />

      {/* Gaslighting Score Display */}
      <div className="flex justify-center">
        <ScoreDisplay
          gaslighting_score={result.gaslighting_score}
          severity_label={result.severity_label}
        />
      </div>
    </div>
  );
}

export default ResultsView;
