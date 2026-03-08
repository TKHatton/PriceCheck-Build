import React from 'react';
import TacticCard from './TacticCard';

function SplitScreen({
  pageTitle,
  marketedPrice,
  realPrice,
  priceDelta,
  realCostNote,
  tactics = []
}) {
  const hasPriceData = marketedPrice !== null || realPrice !== null;

  return (
    <div className="space-y-4">
      {/* Top Section: What They Show */}
      <div className="bg-white border border-rule rounded-lg p-4">
        <h3 className="font-mono text-xs uppercase text-ink-light tracking-wider mb-3">
          WHAT THEY SHOW
        </h3>
        <p className="font-body text-ink text-base font-medium mb-2">
          {pageTitle || 'Product Page'}
        </p>
        {marketedPrice !== null && marketedPrice !== undefined ? (
          <p className="font-display text-2xl font-bold text-ink">
            ${marketedPrice.toFixed(2)}
          </p>
        ) : (
          <p className="font-body text-sm text-ink-light italic">
            {tactics.length > 0 ? 'See manipulation details below' : 'Price not clearly displayed'}
          </p>
        )}
      </div>

      {/* Bottom Section: What Is Really Happening */}
      <div className="bg-red-tint border border-red-mid rounded-lg p-4">
        <h3 className="font-mono text-xs uppercase text-ink-light tracking-wider mb-3">
          WHAT IS REALLY HAPPENING
        </h3>

        {hasPriceData ? (
          <>
            {realPrice !== null && realPrice !== undefined && (
              <p className="font-display text-2xl font-bold text-red-alarm mb-2">
                ${realPrice.toFixed(2)}
              </p>
            )}

            {priceDelta !== null && priceDelta !== undefined && priceDelta > 0 && (
              <p className="font-body text-sm text-red-alarm font-semibold mb-2">
                +${priceDelta.toFixed(2)} more than shown
              </p>
            )}

            {realCostNote && (
              <p className="font-body text-ink-mid" style={{ fontSize: '0.82rem' }}>
                {realCostNote}
              </p>
            )}
          </>
        ) : (
          <p className="font-body text-ink-mid" style={{ fontSize: '0.82rem' }}>
            {tactics.length > 0
              ? `${tactics.length} manipulation ${tactics.length === 1 ? 'tactic' : 'tactics'} detected on this page`
              : 'No pricing manipulation detected'
            }
          </p>
        )}
      </div>

      {/* Tactic Cards with staggered animation */}
      {tactics.length > 0 && (
        <div className="space-y-3">
          <h3 className="font-mono text-xs uppercase text-ink-light tracking-wider">
            MANIPULATION TACTICS DETECTED
          </h3>
          {tactics.map((tactic, index) => (
            <TacticCard
              key={index}
              name={tactic.name}
              severity={tactic.severity}
              evidence={tactic.evidence}
              explanation={tactic.explanation}
              delay={index * 0.08} // 80ms stagger
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default SplitScreen;
