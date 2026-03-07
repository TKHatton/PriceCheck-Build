import React, { useEffect, useState } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';

function ScoreDisplay({ gaslighting_score, severity_label }) {
  const [displayScore, setDisplayScore] = useState(0);

  // Determine color based on score
  const getScoreColor = (score) => {
    if (score <= 20) return '#1A7A4A'; // trust green
    if (score <= 45) return '#C47C00'; // amber
    return '#D42B2B'; // red-alarm
  };

  const scoreColor = getScoreColor(gaslighting_score);

  // Count up animation
  useEffect(() => {
    let startTime;
    const duration = 1200; // 1200ms

    const animate = (currentTime) => {
      if (!startTime) startTime = currentTime;
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function (ease-out)
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(eased * gaslighting_score);

      setDisplayScore(current);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [gaslighting_score]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.5,
        ease: [0.16, 1, 0.3, 1] // ease-reveal
      }}
      className="inline-block p-6 bg-white rounded-lg"
      style={{
        border: '2px solid #D42B2B',
        boxShadow: '4px 4px 0 #D42B2B'
      }}
    >
      {/* Score Number */}
      <div className="flex items-baseline justify-center">
        <span
          className="font-display text-6xl font-bold"
          style={{ color: scoreColor }}
        >
          {displayScore}
        </span>
        <span
          className="font-display text-3xl font-bold text-ink-light ml-1"
        >
          /100
        </span>
      </div>

      {/* Severity Label */}
      <div className="mt-4 text-center">
        <span className="font-mono text-sm uppercase text-ink tracking-wider">
          {severity_label}
        </span>
      </div>
    </motion.div>
  );
}

export default ScoreDisplay;
