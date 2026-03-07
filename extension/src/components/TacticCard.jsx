import React from 'react';
import { motion } from 'framer-motion';

function TacticCard({ name, severity, evidence, explanation, delay = 0 }) {
  // Determine styling based on severity
  const getStyling = () => {
    if (severity >= 7) {
      return {
        borderColor: '#D42B2B', // red-alarm
        backgroundColor: '#FDF1F1', // red-tint
        nameColor: '#D42B2B'
      };
    } else if (severity >= 4) {
      return {
        borderColor: '#C47C00', // amber
        backgroundColor: '#FDF6E8', // amber-tint
        nameColor: '#C47C00'
      };
    } else {
      return {
        borderColor: '#E2E0DA', // rule
        backgroundColor: '#FFFFFF', // white
        nameColor: '#8C8880' // ink-light
      };
    }
  };

  const styling = getStyling();

  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{
        delay: delay,
        duration: 0.5,
        ease: [0.16, 1, 0.3, 1] // ease-reveal
      }}
      className="p-4 rounded"
      style={{
        borderLeft: `3px solid ${styling.borderColor}`,
        backgroundColor: styling.backgroundColor
      }}
    >
      {/* Tactic Name */}
      <h3
        className="font-display text-sm font-bold uppercase mb-2"
        style={{ color: styling.nameColor }}
      >
        {name.replace(/_/g, ' ')}
      </h3>

      {/* Evidence */}
      {evidence && (
        <p
          className="font-mono italic text-ink-light mb-2"
          style={{ fontSize: '0.7rem' }}
        >
          "{evidence}"
        </p>
      )}

      {/* Explanation */}
      <p
        className="font-body text-ink-mid"
        style={{ fontSize: '0.82rem' }}
      >
        {explanation}
      </p>
    </motion.div>
  );
}

export default TacticCard;
