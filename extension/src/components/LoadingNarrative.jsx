import React from 'react';
import { motion } from 'framer-motion';

function LoadingNarrative({ steps }) {
  return (
    <div className="space-y-2">
      {steps.map((step, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            delay: index * 0.7, // 700ms stagger
            duration: 0.4,
            ease: [0.16, 1, 0.3, 1] // ease-reveal from design system
          }}
          className="font-mono text-ink-mid"
          style={{ fontSize: '0.85rem' }}
        >
          {step}
        </motion.div>
      ))}
    </div>
  );
}

export default LoadingNarrative;
