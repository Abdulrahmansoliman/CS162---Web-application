/**
 * Task Display Utilities
 * 
 * ABSTRACTION PRINCIPLE:
 * Encapsulates complex calculations for task display (indentation, colors, etc.)
 * into pure functions. External components use simple function calls instead of
 * implementing this logic themselves.
 * 
 * SINGLE RESPONSIBILITY PRINCIPLE:
 * Each function has ONE job (calculate indentation, get border color, etc.)
 * 
 * PURE FUNCTIONS:
 * All functions are pure - same input always produces same output, no side effects.
 * This makes them easily testable and predictable.
 */

/**
 * Calculate indentation for a task based on its nesting level
 * 
 * BUSINESS RULE:
 * - First 3 levels: 24px per level (0px, 24px, 48px, 72px)
 * - Deeper levels: Add 12px per level (84px, 96px, 108px, etc.)
 * 
 * This provides clear visual hierarchy while preventing excessive indentation
 * for deeply nested tasks.
 * 
 * @param level - Nesting depth (0 = root)
 * @returns Indentation in pixels
 */
export const calculateIndentation = (level: number): number => {
  if (level === 0) return 0;
  if (level <= 3) return level * 24;
  return 72 + ((level - 3) * 12);
};

/**
 * Get border color class based on nesting level
 * 
 * ABSTRACTION: Hides color palette logic from components
 * 
 * Color progression provides visual cues for depth:
 * - Level 0: Primary blue
 * - Level 1: Accent purple  
 * - Level 2: Pink
 * - Level 3+: Gray (to avoid too many colors)
 * 
 * @param level - Nesting depth
 * @returns Tailwind CSS border color class
 */
export const getBorderColor = (level: number): string => {
  const colors = [
    'border-primary-200',  // Level 0 - Blue
    'border-accent-200',   // Level 1 - Purple
    'border-pink-200',     // Level 2 - Pink
    'border-gray-200',     // Level 3+ - Gray
  ];
  
  return colors[Math.min(level, colors.length - 1)];
};

/**
 * Get background hover color based on nesting level
 * 
 * ABSTRACTION: Centralizes hover state styling
 * 
 * @param level - Nesting depth
 * @returns Tailwind CSS hover background class
 */
export const getHoverColor = (level: number): string => {
  const colors = [
    'hover:bg-primary-50',  // Level 0
    'hover:bg-accent-50',   // Level 1
    'hover:bg-pink-50',     // Level 2
    'hover:bg-gray-50',     // Level 3+
  ];
  
  return colors[Math.min(level, colors.length - 1)];
};

/**
 * Cycle to the next priority level
 * 
 * ABSTRACTION: Encapsulates priority cycling logic
 * 
 * Priority cycle: low → medium → high → urgent → low
 * 
 * @param current - Current priority level
 * @returns Next priority in the cycle
 */
export const getNextPriority = (
  current: 'low' | 'medium' | 'high' | 'urgent'
): 'low' | 'medium' | 'high' | 'urgent' => {
  const cycle = {
    low: 'medium',
    medium: 'high',
    high: 'urgent',
    urgent: 'low',
  } as const;
  
  return cycle[current];
};

/**
 * Format a date for display
 * 
 * ABSTRACTION: Centralizes date formatting logic
 * 
 * @param dateString - ISO date string
 * @returns Formatted date (e.g., "Jan 15, 2025")
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};
