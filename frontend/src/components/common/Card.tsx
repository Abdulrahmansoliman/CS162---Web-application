/**
 * Card Component
 * Reusable card container with hover effects
 */

import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  onClick?: () => void;
  className?: string;
  hoverable?: boolean;
}

const Card: React.FC<CardProps> = ({
  children,
  onClick,
  className = '',
  hoverable = true,
}) => {
  return (
    <motion.div
      onClick={onClick}
      className={`
        bg-white rounded-xl shadow-md
        transition-all duration-200
        ${hoverable ? 'hover:shadow-lg cursor-pointer' : ''}
        ${onClick ? 'cursor-pointer' : ''}
        ${className}
      `}
      whileHover={hoverable ? { y: -2 } : {}}
      whileTap={onClick ? { scale: 0.98 } : {}}
    >
      {children}
    </motion.div>
  );
};

export default Card;
