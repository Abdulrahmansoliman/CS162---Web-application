/**
 * Task Item Component
 * Recursive component that displays a task item and its children
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Draggable, Droppable } from '@hello-pangea/dnd';
import {
  IoCheckmarkCircle,
  IoEllipseOutline,
  IoChevronForward,
  IoAdd,
  IoTrash,
  IoCreate,
  IoReorderThree,
  IoSwapHorizontal,
  IoArrowDown,
} from 'react-icons/io5';
import { useTasks } from '@/contexts/TaskContext';
import { TodoItem } from '@/types';
import Button from '@/components/common/Button';
import Modal from '@/components/common/Modal';
import Input from '@/components/common/Input';

interface TaskItemProps {
  item: TodoItem;
  level: number;
  index: number;
}

const TaskItem = ({ item, level, index }: TaskItemProps) => {
  const { lists, toggleComplete, toggleCollapsed, createItem, updateItem, deleteItem, moveItemToList, moveToParent, currentList } = useTasks();
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showMoveModal, setShowMoveModal] = useState(false);
  const [showMoveToParentModal, setShowMoveToParentModal] = useState(false);
  const [newItemTitle, setNewItemTitle] = useState('');
  const [newItemDescription, setNewItemDescription] = useState('');
  const [newItemPriority, setNewItemPriority] = useState<'low' | 'medium' | 'high' | 'urgent'>('medium');
  const [editTitle, setEditTitle] = useState(item.title);
  const [editDescription, setEditDescription] = useState(item.description || '');
  const [editPriority, setEditPriority] = useState(item.priority);
  const [selectedListId, setSelectedListId] = useState<number | null>(null);
  const [selectedParentId, setSelectedParentId] = useState<number | null>(null);

  const hasChildren = item.children && item.children.length > 0;
  // Allow infinite nesting - always show add button
  const canAddChild = true;

  const handleToggleComplete = async () => {
    await toggleComplete(item.id, item.is_completed);
  };

  const handleToggleCollapse = async () => {
    if (hasChildren) {
      await toggleCollapsed(item.id, item.is_collapsed);
    }
  };

  const handleAddChild = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newItemTitle.trim()) return;

    try {
      await createItem({
        list_id: item.list_id,
        title: newItemTitle,
        description: newItemDescription || undefined,
        priority: newItemPriority,
        parent_id: item.id,
      });
      setNewItemTitle('');
      setNewItemDescription('');
      setNewItemPriority('medium');
      setShowAddModal(false);
    } catch (error) {
      // Error handled by context
    }
  };

  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editTitle.trim()) return;

    try {
      await updateItem(item.id, {
        title: editTitle,
        description: editDescription || undefined,
        priority: editPriority,
      });
      setShowEditModal(false);
    } catch (error) {
      // Error handled by context
    }
  };

  const handleDelete = async () => {
    if (!confirm('Delete this task and all its subtasks?')) return;
    await deleteItem(item.id);
  };

  const handleMoveToList = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedListId === null) return;

    try {
      await moveItemToList(item.id, selectedListId);
      setShowMoveModal(false);
      setSelectedListId(null);
    } catch (error) {
      // Error handled by context
    }
  };

  const handleMoveToParent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // selectedParentId can be null (moves to root level)
      await moveToParent(item.id, selectedParentId);
      setShowMoveToParentModal(false);
      setSelectedParentId(null);
    } catch (error) {
      // Error handled by context
    }
  };

  // Smart indentation: smaller increments for deep nesting
  // First 3 levels: 24px each, then 12px for deeper levels
  const getIndentation = (level: number) => {
    if (level === 0) return 0;
    if (level <= 3) return level * 24;
    return 72 + (level - 3) * 12; // 3 * 24 + additional smaller increments
  };

  const marginLeft = getIndentation(level);

  // Visual depth indicator - different border colors for levels
  const getBorderStyle = (level: number) => {
    const colors = [
      'border-gray-200',      // Level 0
      'border-blue-100',      // Level 1
      'border-purple-100',    // Level 2
      'border-pink-100',      // Level 3
      'border-orange-100',    // Level 4+
    ];
    return colors[Math.min(level, colors.length - 1)];
  };

  const getLeftBorderColor = (level: number) => {
    const colors = [
      'border-l-primary-400',   // Level 0
      'border-l-blue-400',      // Level 1
      'border-l-purple-400',    // Level 2
      'border-l-pink-400',      // Level 3
      'border-l-orange-400',    // Level 4+
    ];
    return colors[Math.min(level, colors.length - 1)];
  };

  return (
    <>
      <Draggable draggableId={`task-${item.id}`} index={index}>
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.draggableProps}
          >
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.2 }}
              style={{ marginLeft: `${marginLeft}px` }}
              className={`group ${item.is_completed ? 'opacity-60' : ''} ${snapshot.isDragging ? 'opacity-50' : ''}`}
            >
              <div
                className={`
                  flex items-center gap-3 px-4 py-3 rounded-lg
                  bg-white border-2 border-l-4 transition-all duration-200
                  hover:shadow-md hover:border-primary-300
                  ${getBorderStyle(level)}
                  ${getLeftBorderColor(level)}
                  ${item.is_completed ? 'border-gray-200' : ''}
                  ${snapshot.isDragging ? 'shadow-lg rotate-2' : ''}
                `}
              >
          {/* Drag Handle */}
          <div
            {...provided.dragHandleProps}
            className="text-gray-400 hover:text-gray-600 cursor-grab active:cursor-grabbing opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <IoReorderThree size={20} />
          </div>

          {/* Collapse/Expand Button */}
          {hasChildren && (
            <button
              onClick={handleToggleCollapse}
              className="text-gray-500 hover:text-primary-600 transition-colors"
            >
              <motion.div
                animate={{ rotate: item.is_collapsed ? 0 : 90 }}
                transition={{ duration: 0.2 }}
              >
                <IoChevronForward size={18} />
              </motion.div>
            </button>
          )}

          {/* Complete/Incomplete Checkbox */}
          <button
            onClick={handleToggleComplete}
            className={`
              text-2xl transition-all duration-200 transform hover:scale-110
              ${
                item.is_completed
                  ? 'text-green-500'
                  : 'text-gray-300 hover:text-green-500'
              }
            `}
          >
            {item.is_completed ? (
              <IoCheckmarkCircle />
            ) : (
              <IoEllipseOutline />
            )}
          </button>

          {/* Task Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              {/* Priority badge with click to change */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  const priorities: Array<'low' | 'medium' | 'high' | 'urgent'> = ['low', 'medium', 'high', 'urgent'];
                  const currentIndex = priorities.indexOf(item.priority);
                  const nextPriority = priorities[(currentIndex + 1) % priorities.length];
                  updateItem(item.id, { priority: nextPriority });
                }}
                className={`
                  px-2 py-0.5 text-xs rounded-full font-semibold flex-shrink-0
                  transition-all duration-200 hover:scale-105 cursor-pointer
                  ${item.priority === 'low' ? 'bg-gray-100 text-gray-600 hover:bg-gray-200' : ''}
                  ${item.priority === 'medium' ? 'bg-blue-100 text-blue-700 hover:bg-blue-200' : ''}
                  ${item.priority === 'high' ? 'bg-orange-100 text-orange-700 hover:bg-orange-200' : ''}
                  ${item.priority === 'urgent' ? 'bg-red-100 text-red-700 hover:bg-red-200' : ''}
                `}
                title="Click to change priority"
              >
                {item.priority === 'low' && '⬇️ Low'}
                {item.priority === 'medium' && '➡️ Medium'}
                {item.priority === 'high' && '⬆️ High'}
                {item.priority === 'urgent' && '🔥 Urgent'}
              </button>

              {/* Depth badge showing nesting level */}
              <span className={`
                px-2 py-0.5 text-xs rounded-full font-mono flex-shrink-0
                ${level === 0 ? 'bg-blue-100 text-blue-700' : ''}
                ${level === 1 ? 'bg-purple-100 text-purple-700' : ''}
                ${level === 2 ? 'bg-pink-100 text-pink-700' : ''}
                ${level === 3 ? 'bg-orange-100 text-orange-700' : ''}
                ${level >= 4 ? 'bg-gray-100 text-gray-700' : ''}
              `}>
                Level {level}
              </span>
              <h3
                className={`
                  font-medium break-words
                  ${item.is_completed ? 'line-through text-gray-500' : 'text-gray-900'}
                `}
              >
                {item.title}
              </h3>
            </div>
            {item.description && (
              <p className="text-sm text-gray-600 mt-1">{item.description}</p>
            )}
          </div>

          {/* Action Buttons (shown on hover) */}
          <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            {canAddChild && (
              <Button
                onClick={() => setShowAddModal(true)}
                variant="ghost"
                size="small"
                icon={<IoAdd size={18} />}
              />
            )}
            {level === 0 && (
              <Button
                onClick={() => setShowMoveModal(true)}
                variant="ghost"
                size="small"
                icon={<IoSwapHorizontal size={18} />}
              />
            )}
            <Button
              onClick={() => setShowMoveToParentModal(true)}
              variant="ghost"
              size="small"
              icon={<IoArrowDown size={18} />}
            />
            <Button
              onClick={() => {
                setEditTitle(item.title);
                setEditDescription(item.description || '');
                setEditPriority(item.priority);
                setShowEditModal(true);
              }}
              variant="ghost"
              size="small"
              icon={<IoCreate size={18} />}
            />
            <Button
              onClick={handleDelete}
              variant="ghost"
              size="small"
              icon={<IoTrash size={18} />}
            />
          </div>
        </div>
      </motion.div>

      {/* Render Children (Recursively) with Droppable */}
      {/* Drop zone to make this task a parent */}
      <Droppable droppableId={`parent-${item.id}`} type="task">
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className={`
              mt-1 rounded-md transition-all
              ${snapshot.isDraggingOver ? 'bg-blue-50 border-2 border-dashed border-blue-300 py-2' : ''}
              ${hasChildren && !item.is_collapsed ? 'space-y-2' : ''}
            `}
          >
            {/* Show visual indicator when dragging over */}
            {snapshot.isDraggingOver && !hasChildren && (
              <div className="px-4 py-2 text-sm text-blue-600 font-medium">
                Drop here to make it a subtask
              </div>
            )}
            
            {/* Render existing children */}
            <AnimatePresence>
              {hasChildren && !item.is_collapsed && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-2"
                  style={{ marginLeft: '0px' }}
                >
                  {item.children!.map((child, childIndex) => (
                    <TaskItem key={child.id} item={child} level={level + 1} index={childIndex} />
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
            
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
        )}
      </Draggable>
    
      {/* Modals (outside of Draggable to prevent drag interference) */}
      {/* Add Child Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add Subtask"
        size="medium"
      >
        <form onSubmit={handleAddChild} className="space-y-4">
          <Input
            label="Subtask Title"
            placeholder="What needs to be done?"
            value={newItemTitle}
            onChange={(e) => setNewItemTitle(e.target.value)}
            autoFocus
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description (optional)
            </label>
            <textarea
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
              rows={3}
              placeholder="Add more details..."
              value={newItemDescription}
              onChange={(e) => setNewItemDescription(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <div className="grid grid-cols-4 gap-2">
              <button
                type="button"
                onClick={() => setNewItemPriority('low')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  newItemPriority === 'low'
                    ? 'border-gray-400 bg-gray-100 text-gray-700 font-semibold'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                ⬇️ Low
              </button>
              <button
                type="button"
                onClick={() => setNewItemPriority('medium')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  newItemPriority === 'medium'
                    ? 'border-blue-400 bg-blue-100 text-blue-700 font-semibold'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                ➡️ Medium
              </button>
              <button
                type="button"
                onClick={() => setNewItemPriority('high')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  newItemPriority === 'high'
                    ? 'border-orange-400 bg-orange-100 text-orange-700 font-semibold'
                    : 'border-gray-200 hover:border-orange-300'
                }`}
              >
                ⬆️ High
              </button>
              <button
                type="button"
                onClick={() => setNewItemPriority('urgent')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  newItemPriority === 'urgent'
                    ? 'border-red-400 bg-red-100 text-red-700 font-semibold'
                    : 'border-gray-200 hover:border-red-300'
                }`}
              >
                🔥 Urgent
              </button>
            </div>
          </div>
          <div className="flex gap-3">
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={() => setShowAddModal(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              fullWidth
              disabled={!newItemTitle.trim()}
            >
              Add Subtask
            </Button>
          </div>
        </form>
      </Modal>

      {/* Edit Modal */}
      <Modal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        title="Edit Task"
        size="medium"
      >
        <form onSubmit={handleEdit} className="space-y-4">
          <Input
            label="Task Title"
            placeholder="What needs to be done?"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            autoFocus
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description (optional)
            </label>
            <textarea
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
              rows={3}
              placeholder="Add more details..."
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <div className="grid grid-cols-4 gap-2">
              <button
                type="button"
                onClick={() => setEditPriority('low')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  editPriority === 'low'
                    ? 'border-gray-400 bg-gray-100 text-gray-700 font-semibold'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                ⬇️ Low
              </button>
              <button
                type="button"
                onClick={() => setEditPriority('medium')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  editPriority === 'medium'
                    ? 'border-blue-400 bg-blue-100 text-blue-700 font-semibold'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                ➡️ Medium
              </button>
              <button
                type="button"
                onClick={() => setEditPriority('high')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  editPriority === 'high'
                    ? 'border-orange-400 bg-orange-100 text-orange-700 font-semibold'
                    : 'border-gray-200 hover:border-orange-300'
                }`}
              >
                ⬆️ High
              </button>
              <button
                type="button"
                onClick={() => setEditPriority('urgent')}
                className={`px-3 py-2 text-sm rounded-lg border-2 transition-all ${
                  editPriority === 'urgent'
                    ? 'border-red-400 bg-red-100 text-red-700 font-semibold'
                    : 'border-gray-200 hover:border-red-300'
                }`}
              >
                🔥 Urgent
              </button>
            </div>
          </div>
          <div className="flex gap-3">
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={() => setShowEditModal(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              fullWidth
              disabled={!editTitle.trim()}
            >
              Save Changes
            </Button>
          </div>
        </form>
      </Modal>

      {/* Move to List Modal */}
      <Modal
        isOpen={showMoveModal}
        onClose={() => {
          setShowMoveModal(false);
          setSelectedListId(null);
        }}
        title="Move Task to Another List"
        size="medium"
      >
        <form onSubmit={handleMoveToList} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select target list
            </label>
            <p className="text-sm text-gray-600 mb-3">
              This will move "{item.title}" and all its subtasks to the selected list.
            </p>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
              value={selectedListId || ''}
              onChange={(e) => setSelectedListId(e.target.value ? Number(e.target.value) : null)}
              required
            >
              <option value="">-- Select a list --</option>
              {lists
                .filter(list => list.id !== item.list_id)
                .map(list => (
                  <option key={list.id} value={list.id}>
                    {list.title}
                  </option>
                ))}
            </select>
          </div>
          <div className="flex gap-3">
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={() => {
                setShowMoveModal(false);
                setSelectedListId(null);
              }}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              fullWidth
              disabled={selectedListId === null}
            >
              Move Task
            </Button>
          </div>
        </form>
      </Modal>

      {/* Move to Parent Modal - Move task to be a subtask of another task */}
      <Modal
        isOpen={showMoveToParentModal}
        onClose={() => {
          setShowMoveToParentModal(false);
          setSelectedParentId(null);
        }}
        title="Move Task to Another Task"
        size="medium"
      >
        <form onSubmit={handleMoveToParent} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select target parent task
            </label>
            <p className="text-sm text-gray-600 mb-3">
              Move "{item.title}" to be a subtask of another task, or select "Root Level" to move it to the top level.
            </p>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
              value={selectedParentId ?? ''}
              onChange={(e) => setSelectedParentId(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">-- Root Level (No Parent) --</option>
              {currentList && currentList.items ? (
                (() => {
                  // Helper function to flatten all tasks recursively
                  const flattenTasks = (tasks: TodoItem[], prefix = ''): JSX.Element[] => {
                    return tasks.flatMap(task => {
                      // Don't allow task to be its own parent
                      if (task.id === item.id) return [];
                      
                      const option = (
                        <option key={task.id} value={task.id}>
                          {prefix}{task.title}
                        </option>
                      );
                      
                      // Add children recursively
                      if (task.children && task.children.length > 0) {
                        return [option, ...flattenTasks(task.children, prefix + '  └─ ')];
                      }
                      return [option];
                    });
                  };
                  
                  return flattenTasks(currentList.items);
                })()
              ) : null}
            </select>
          </div>
          <div className="flex gap-3">
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={() => {
                setShowMoveToParentModal(false);
                setSelectedParentId(null);
              }}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              fullWidth
            >
              Move Task
            </Button>
          </div>
        </form>
      </Modal>
    </>
  );
};

export default TaskItem;
