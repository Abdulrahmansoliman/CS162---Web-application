/**
 * Priority Badge Component
 * 
 * ABSTRACTION PRINCIPLE:
 * Extracts priority display logic into a reusable component that hides
 * the implementation details of how priorities are rendered and cycled.
 * 
 * SINGLE RESPONSIBILITY PRINCIPLE:
 * This component has ONE responsibility: Display and cycle through priority levels.
 * It doesn't handle task updates, API calls, or other business logic.
 */

import { TodoItem } from '@/types';

interface PriorityBadgeProps {
  priority: TodoItem['priority'];
  onCycle: () => void;
  className?: string;
}

/**
 * Priority configuration object
 * Demonstrates ABSTRACTION by encapsulating priority metadata
 */
const PRIORITY_CONFIG = {
  low: { emoji: '⬇️', label: 'Low', color: 'text-gray-600 bg-gray-100' },
  medium: { emoji: '➡️', label: 'Medium', color: 'text-blue-600 bg-blue-100' },
  high: { emoji: '⬆️', label: 'High', color: 'text-orange-600 bg-orange-100' },
  urgent: { emoji: '🔥', label: 'Urgent', color: 'text-red-600 bg-red-100' },
} as const;

/**
 * PriorityBadge Component
 * 
 * Renders a clickable badge showing the task's priority level.
 * Clicking cycles through: low → medium → high → urgent → low
 * 
 * @param priority - Current priority level
 * @param onCycle - Callback when user clicks to cycle priority
 * @param className - Optional additional CSS classes
 */
const PriorityBadge = ({ priority, onCycle, className = '' }: PriorityBadgeProps) => {
  const config = PRIORITY_CONFIG[priority];

  return (
    <button
      onClick={onCycle}
      className={`
        px-2 py-1 rounded-lg text-xs font-medium transition-all
        hover:scale-105 active:scale-95
        ${config.color}
        ${className}
      `}
      title="Click to cycle priority"
    >
      <span className="mr-1">{config.emoji}</span>
      {config.label}
    </button>
  );
};

export default PriorityBadge;
