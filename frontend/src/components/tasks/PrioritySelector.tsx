/**
 * Priority Selector Component
 * 
 * ABSTRACTION PRINCIPLE:
 * Abstracts the UI for selecting priority levels into a reusable component.
 * Users of this component don't need to know the implementation details
 * of how priorities are displayed or selected.
 * 
 * SINGLE RESPONSIBILITY PRINCIPLE:
 * One responsibility: Allow users to select a priority level from 4 options.
 * Doesn't handle saving, validation, or other business logic.
 * 
 * REUSABILITY:
 * Can be used in Add Task modal, Edit Task modal, or anywhere priority selection is needed.
 */

import { TodoItem } from '@/types';

interface PrioritySelectorProps {
  selectedPriority: TodoItem['priority'];
  onSelect: (priority: TodoItem['priority']) => void;
  className?: string;
}

/**
 * Priority option configuration
 * Demonstrates ABSTRACTION by centralizing priority metadata
 */
const PRIORITY_OPTIONS = [
  { value: 'low' as const, emoji: '⬇️', label: 'Low', color: 'gray' },
  { value: 'medium' as const, emoji: '➡️', label: 'Medium', color: 'blue' },
  { value: 'high' as const, emoji: '⬆️', label: 'High', color: 'orange' },
  { value: 'urgent' as const, emoji: '🔥', label: 'Urgent', color: 'red' },
];

/**
 * PrioritySelector Component
 * 
 * Renders a 4-button grid for selecting task priority.
 * Highlights the currently selected priority with stronger colors.
 * 
 * @param selectedPriority - Currently selected priority
 * @param onSelect - Callback when a priority is selected
 * @param className - Optional additional CSS classes
 */
const PrioritySelector = ({ 
  selectedPriority, 
  onSelect, 
  className = '' 
}: PrioritySelectorProps) => {
  /**
   * Get button styling based on selection state
   * 
   * ABSTRACTION: Hides the complexity of conditional styling
   */
  const getButtonClass = (value: string, color: string): string => {
    const isSelected = selectedPriority === value;
    
    const baseClass = 'px-3 py-2 text-sm rounded-lg border-2 transition-all';
    const hoverClass = 'hover:scale-105 active:scale-95';
    
    // Selected state: Bold border and background
    if (isSelected) {
      const colorMap: Record<string, string> = {
        gray: 'border-gray-400 bg-gray-100 text-gray-700 font-semibold',
        blue: 'border-blue-400 bg-blue-100 text-blue-700 font-semibold',
        orange: 'border-orange-400 bg-orange-100 text-orange-700 font-semibold',
        red: 'border-red-400 bg-red-100 text-red-700 font-semibold',
      };
      return `${baseClass} ${colorMap[color]} ${hoverClass}`;
    }
    
    // Unselected state: Subtle border
    return `${baseClass} border-gray-200 hover:border-gray-300 ${hoverClass}`;
  };

  return (
    <div className={`grid grid-cols-4 gap-2 ${className}`}>
      {PRIORITY_OPTIONS.map(({ value, emoji, label, color }) => (
        <button
          key={value}
          type="button"
          onClick={() => onSelect(value)}
          className={getButtonClass(value, color)}
          title={`Set priority to ${label}`}
        >
          <span className="block text-lg mb-1">{emoji}</span>
          <span className="block text-xs">{label}</span>
        </button>
      ))}
    </div>
  );
};

export default PrioritySelector;
