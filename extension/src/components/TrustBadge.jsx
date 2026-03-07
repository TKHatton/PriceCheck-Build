import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

function TrustBadge({ trustScore }) {
  const [isVisible, setIsVisible] = useState(true);

  // Determine badge state
  const getBadgeState = () => {
    if (trustScore >= 70) {
      return 'PASS';
    } else if (trustScore >= 30) {
      return 'WARN';
    } else {
      return 'FAIL'; // Don't render - ScamView handles this
    }
  };

  const state = getBadgeState();

  // Fade out PASS state after 2000ms
  useEffect(() => {
    if (state === 'PASS') {
      const timer = setTimeout(() => {
        setIsVisible(false);
      }, 2000);

      return () => clearTimeout(timer);
    }
  }, [state]);

  // Don't render for FAIL state
  if (state === 'FAIL') {
    return null;
  }

  // PASS state: green pill that fades out
  if (state === 'PASS') {
    return (
      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{
              duration: 0.4,
              ease: [0.16, 1, 0.3, 1]
            }}
            className="inline-flex items-center px-4 py-2 rounded-full"
            style={{
              backgroundColor: '#EDF7F2', // trust-tint
              border: '1px solid #1A7A4A' // trust
            }}
          >
            <span
              className="font-mono text-xs font-semibold"
              style={{ color: '#1A7A4A' }} // trust
            >
              Verified Retailer
            </span>
          </motion.div>
        )}
      </AnimatePresence>
    );
  }

  // WARN state: amber persistent notice
  if (state === 'WARN') {
    return (
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{
          duration: 0.4,
          ease: [0.16, 1, 0.3, 1]
        }}
        className="p-3 rounded-lg"
        style={{
          backgroundColor: '#FDF6E8', // amber-tint
          border: '2px solid #C47C00' // amber
        }}
      >
        <div className="flex items-center gap-2">
          <span className="text-lg">⚠️</span>
          <span
            className="font-body text-sm font-semibold"
            style={{ color: '#C47C00' }} // amber
          >
            Could not fully verify this retailer
          </span>
        </div>
      </motion.div>
    );
  }

  return null;
}

export default TrustBadge;
