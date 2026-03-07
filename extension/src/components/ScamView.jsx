import React from 'react';
import { motion } from 'framer-motion';

function ScamView({ trustSignals = [] }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.5,
        ease: [0.16, 1, 0.3, 1]
      }}
      className="mt-6"
    >
      {/* Main warning box - white background with heavy red border for readability */}
      <div
        className="p-6 rounded-lg bg-white"
        style={{
          border: '4px solid #D42B2B', // red-alarm
          boxShadow: '0 4px 12px rgba(212, 43, 43, 0.15)'
        }}
      >
        {/* Warning Icon */}
        <div className="text-center mb-4">
          <span className="text-5xl">🚨</span>
        </div>

        {/* Main Heading */}
        <h2 className="font-display text-2xl font-bold text-red-alarm text-center uppercase mb-3">
          This Site Raised Fraud Signals
        </h2>

        {/* Subheading */}
        <p className="font-body text-base text-ink text-center mb-6 leading-relaxed">
          We recommend not entering payment information on this site
        </p>

        {/* Divider */}
        <div className="border-t border-rule my-4"></div>

        {/* Trust Signals List */}
        {trustSignals.length > 0 && (
          <div>
            <h3 className="font-mono text-xs uppercase text-ink-light tracking-wider mb-3">
              RED FLAGS DETECTED:
            </h3>
            <ul className="space-y-2">
              {trustSignals.map((signal, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{
                    delay: index * 0.1,
                    duration: 0.3
                  }}
                  className="flex items-start gap-2"
                >
                  <span className="text-red-alarm mt-1">•</span>
                  <span className="font-body text-sm text-ink-mid flex-1">
                    {signal}
                  </span>
                </motion.li>
              ))}
            </ul>
          </div>
        )}

        {/* Disclaimer */}
        <div className="mt-6 pt-4 border-t border-rule">
          <p className="font-body text-xs text-ink-light text-center leading-relaxed">
            This is a warning, not a guarantee. Proceed with your own judgment.
          </p>
        </div>
      </div>
    </motion.div>
  );
}

export default ScamView;
