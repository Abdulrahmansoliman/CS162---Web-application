/**
 * Depth Badge Component
 * 
 * ABSTRACTION PRINCIPLE:
 * Encapsulates the logic for displaying hierarchical depth levels.
 * External components don't need to know HOW depth is calculated or styled.
 * 
 * SINGLE RESPONSIBILITY PRINCIPLE:
 * One job: Show the nesting level of a task in a color-coded badge.
 */

interface DepthBadgeProps {
  level: number;
  className?: string;
}

/**
 * Depth color mapping
 * Demonstrates ABSTRACTION by hiding complexity of color selection
 */
const DEPTH_COLORS = [
  'bg-blue-100 text-blue-700',    // Level 0
  'bg-purple-100 text-purple-700', // Level 1
  'bg-pink-100 text-pink-700',     // Level 2
  'bg-orange-100 text-orange-700', // Level 3
  'bg-gray-100 text-gray-700',     // Level 4+
] as const;

/**
 * Get color class for a specific depth level
 * 
 * ABSTRACTION: Hides the logic of color selection from consumers
 * 
 * @param level - Nesting depth (0 = root, 1 = first child, etc.)
 * @returns CSS classes for the badge color
 */
const getDepthColor = (level: number): string => {
  return level < DEPTH_COLORS.length 
    ? DEPTH_COLORS[level]
    : DEPTH_COLORS[DEPTH_COLORS.length - 1];
};

/**
 * DepthBadge Component
 * 
 * Displays the hierarchical level of a task item.
 * Colors change based on depth to provide visual hierarchy cues.
 * 
 * @param level - The nesting depth (0 = top-level)
 * @param className - Optional additional CSS classes
 */
const DepthBadge = ({ level, className = '' }: DepthBadgeProps) => {
  return (
    <span
      className={`
        px-2 py-1 rounded text-xs font-semibold
        ${getDepthColor(level)}
        ${className}
      `}
      title={`Nesting level: ${level}`}
    >
      Level {level}
    </span>
  );
};

export default DepthBadge;
