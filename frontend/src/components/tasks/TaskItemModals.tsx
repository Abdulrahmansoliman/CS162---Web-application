/**
 * Task Item Modals Component
 * 
 * SINGLE RESPONSIBILITY PRINCIPLE:
 * This component's ONLY job is rendering the three modals for task management:
 * 1. Add Child Modal
 * 2. Edit Task Modal
 * 3. Move to List Modal
 * 
 * ABSTRACTION PRINCIPLE:
 * Abstracts all modal UI logic away from the main TaskItem component.
 * TaskItem only needs to pass props and callbacks.
 * 
 * MODULARITY:
 * Extracted from TaskItem (600+ lines) to improve maintainability.
 * Each modal is self-contained with its own form logic.
 */

import Modal from '@/components/common/Modal';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import PrioritySelector from './PrioritySelector';
import { IoAdd, IoSave, IoSwapHorizontal } from 'react-icons/io5';
import { TodoItem, TodoList } from '@/types';

interface TaskItemModalsProps {
  // Add Child Modal
  showAddModal: boolean;
  newItemTitle: string;
  newItemDescription: string;
  newItemPriority: TodoItem['priority'];
  onAddModalClose: () => void;
  onNewItemTitleChange: (value: string) => void;
  onNewItemDescriptionChange: (value: string) => void;
  onNewItemPriorityChange: (priority: TodoItem['priority']) => void;
  onAddChildSubmit: (e: React.FormEvent) => void;

  // Edit Modal
  showEditModal: boolean;
  editTitle: string;
  editDescription: string;
  editPriority: TodoItem['priority'];
  onEditModalClose: () => void;
  onEditTitleChange: (value: string) => void;
  onEditDescriptionChange: (value: string) => void;
  onEditPriorityChange: (priority: TodoItem['priority']) => void;
  onEditSubmit: (e: React.FormEvent) => void;

  // Move to List Modal
  showMoveModal: boolean;
  selectedListId: number | null;
  availableLists: TodoList[];
  currentListId: number;
  onMoveModalClose: () => void;
  onSelectedListChange: (listId: number) => void;
  onMoveSubmit: (e: React.FormEvent) => void;
}

/**
 * TaskItemModals Component
 * 
 * Renders three modals for task management operations.
 * All form state and callbacks are controlled by the parent component.
 * 
 * SEPARATION OF CONCERNS:
 * - This component: UI rendering
 * - Parent component: State management and business logic
 */
const TaskItemModals = ({
  // Add Modal props
  showAddModal,
  newItemTitle,
  newItemDescription,
  newItemPriority,
  onAddModalClose,
  onNewItemTitleChange,
  onNewItemDescriptionChange,
  onNewItemPriorityChange,
  onAddChildSubmit,

  // Edit Modal props
  showEditModal,
  editTitle,
  editDescription,
  editPriority,
  onEditModalClose,
  onEditTitleChange,
  onEditDescriptionChange,
  onEditPriorityChange,
  onEditSubmit,

  // Move Modal props
  showMoveModal,
  selectedListId,
  availableLists,
  currentListId,
  onMoveModalClose,
  onSelectedListChange,
  onMoveSubmit,
}: TaskItemModalsProps) => {
  return (
    <>
      {/* ========================================
          ADD CHILD TASK MODAL
          ======================================== */}
      <Modal
        isOpen={showAddModal}
        onClose={onAddModalClose}
        title="Add Subtask"
      >
        <form onSubmit={onAddChildSubmit} className="space-y-4">
          <Input
            label="Title"
            value={newItemTitle}
            onChange={(e) => onNewItemTitleChange(e.target.value)}
            placeholder="Enter subtask title"
            required
            autoFocus
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description (Optional)
            </label>
            <textarea
              value={newItemDescription}
              onChange={(e) => onNewItemDescriptionChange(e.target.value)}
              placeholder="Enter subtask description"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={3}
            />
          </div>

          {/* Priority Selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <PrioritySelector
              selectedPriority={newItemPriority}
              onSelect={onNewItemPriorityChange}
            />
          </div>

          {/* Submit Button */}
          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={onAddModalClose}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              icon={<IoAdd size={18} />}
            >
              Add Subtask
            </Button>
          </div>
        </form>
      </Modal>

      {/* ========================================
          EDIT TASK MODAL
          ======================================== */}
      <Modal
        isOpen={showEditModal}
        onClose={onEditModalClose}
        title="Edit Task"
      >
        <form onSubmit={onEditSubmit} className="space-y-4">
          <Input
            label="Title"
            value={editTitle}
            onChange={(e) => onEditTitleChange(e.target.value)}
            placeholder="Enter task title"
            required
            autoFocus
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description (Optional)
            </label>
            <textarea
              value={editDescription}
              onChange={(e) => onEditDescriptionChange(e.target.value)}
              placeholder="Enter task description"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={3}
            />
          </div>

          {/* Priority Selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <PrioritySelector
              selectedPriority={editPriority}
              onSelect={onEditPriorityChange}
            />
          </div>

          {/* Submit Button */}
          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={onEditModalClose}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              icon={<IoSave size={18} />}
            >
              Save Changes
            </Button>
          </div>
        </form>
      </Modal>

      {/* ========================================
          MOVE TO LIST MODAL
          ======================================== */}
      <Modal
        isOpen={showMoveModal}
        onClose={onMoveModalClose}
        title="Move Task to Another List"
      >
        <form onSubmit={onMoveSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Target List
            </label>
            <select
              value={selectedListId || ''}
              onChange={(e) => onSelectedListChange(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              required
            >
              <option value="">-- Select a list --</option>
              {availableLists
                .filter((list) => list.id !== currentListId)
                .map((list) => (
                  <option key={list.id} value={list.id}>
                    {list.title}
                  </option>
                ))}
            </select>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={onMoveModalClose}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              icon={<IoSwapHorizontal size={18} />}
            >
              Move Task
            </Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

export default TaskItemModals;
