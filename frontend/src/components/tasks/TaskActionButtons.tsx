/**
 * Task Action Buttons Component
 * 
 * SINGLE RESPONSIBILITY PRINCIPLE:
 * This component's SOLE responsibility is rendering action buttons for a task.
 * It doesn't handle business logic, just delegates to callbacks.
 * 
 * ABSTRACTION PRINCIPLE:
 * Abstracts the complex button layout into a simple interface.
 * Parent components just pass callbacks, don't worry about button styling.
 * 
 * MODULARITY:
 * Extracted from TaskItem to reduce complexity and improve maintainability.
 */

import { IoAdd, IoTrash, IoCreate, IoSwapHorizontal } from 'react-icons/io5';
import Button from '@/components/common/Button';

interface TaskActionButtonsProps {
  /** Whether this task can have child tasks added */
  canAddChild: boolean;
  
  /** Whether this is a root-level task (level 0) */
  isRootLevel: boolean;
  
  /** Callback when "Add Subtask" is clicked */
  onAddChild: () => void;
  
  /** Callback when "Edit" is clicked */
  onEdit: () => void;
  
  /** Callback when "Delete" is clicked */
  onDelete: () => void;
  
  /** Callback when "Move to List" is clicked */
  onMoveToList: () => void;
}

/**
 * TaskActionButtons Component
 * 
 * Renders the action buttons for a task item:
 * - Add Subtask (if nesting allowed)
 * - Edit
 * - Move to List (only for root-level tasks)
 * - Delete
 * 
 * SEPARATION OF CONCERNS:
 * This component only handles UI rendering.
 * All business logic is in the parent component's callbacks.
 */
const TaskActionButtons = ({
  canAddChild,
  isRootLevel,
  onAddChild,
  onEdit,
  onDelete,
  onMoveToList,
}: TaskActionButtonsProps) => {
  return (
    <div className="flex gap-2 mt-3">
      {/* Add Child Button - Visible if infinite nesting is enabled */}
      {canAddChild && (
        <Button
          onClick={onAddChild}
          variant="secondary"
          size="small"
          icon={<IoAdd size={14} />}
        >
          Add Subtask
        </Button>
      )}

      {/* Edit Button - Always visible */}
      <Button
        onClick={onEdit}
        variant="secondary"
        size="small"
        icon={<IoCreate size={14} />}
      >
        Edit
      </Button>

      {/* Move to List Button - Only for root-level tasks (level 0) */}
      {isRootLevel && (
        <Button
          onClick={onMoveToList}
          variant="secondary"
          size="small"
          icon={<IoSwapHorizontal size={14} />}
        >
          Move to List
        </Button>
      )}

      {/* Delete Button - Always visible */}
      <Button
        onClick={onDelete}
        variant="danger"
        size="small"
        icon={<IoTrash size={14} />}
      >
        Delete
      </Button>
    </div>
  );
};

export default TaskActionButtons;
