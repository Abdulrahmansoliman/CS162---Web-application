/**
 * Task Item Component
 * Recursive component that displays a task item and its children
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  IoCheckmarkCircle,
  IoEllipseOutline,
  IoChevronForward,
  IoAdd,
  IoTrash,
  IoCreate,
} from 'react-icons/io5';
import { useTasks } from '@/contexts/TaskContext';
import { TodoItem } from '@/types';
import Button from '@/components/common/Button';
import Modal from '@/components/common/Modal';
import Input from '@/components/common/Input';

interface TaskItemProps {
  item: TodoItem;
  level: number;
}

const TaskItem = ({ item, level }: TaskItemProps) => {
  const { toggleComplete, toggleCollapsed, createItem, updateItem, deleteItem } = useTasks();
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [newItemTitle, setNewItemTitle] = useState('');
  const [newItemDescription, setNewItemDescription] = useState('');
  const [editTitle, setEditTitle] = useState(item.title);
  const [editDescription, setEditDescription] = useState(item.description || '');

  const hasChildren = item.children && item.children.length > 0;
  const canAddChild = level < 2; // Max 3 levels (0, 1, 2)

  const handleToggleComplete = async () => {
    await toggleComplete(item.id, !item.is_completed);
  };

  const handleToggleCollapse = async () => {
    if (hasChildren) {
      await toggleCollapsed(item.id, !item.is_collapsed);
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
        parent_id: item.id,
      });
      setNewItemTitle('');
      setNewItemDescription('');
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

  // Indentation based on level
  const marginLeft = level * 24;

  return (
    <>
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.2 }}
        style={{ marginLeft: `${marginLeft}px` }}
        className={`group ${item.is_completed ? 'opacity-60' : ''}`}
      >
        <div
          className={`
            flex items-center gap-3 px-4 py-3 rounded-lg
            bg-white border-2 transition-all duration-200
            hover:shadow-md hover:border-primary-300
            ${item.is_completed ? 'border-gray-200' : 'border-gray-200'}
          `}
        >
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
            <h3
              className={`
                font-medium
                ${item.is_completed ? 'line-through text-gray-500' : 'text-gray-900'}
              `}
            >
              {item.title}
            </h3>
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
            <Button
              onClick={() => {
                setEditTitle(item.title);
                setEditDescription(item.description || '');
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

      {/* Render Children (Recursively) */}
      <AnimatePresence>
        {hasChildren && !item.is_collapsed && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="mt-2 space-y-2"
          >
            {item.children!.map((child) => (
              <TaskItem key={child.id} item={child} level={level + 1} />
            ))}
          </motion.div>
        )}
      </AnimatePresence>

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
    </>
  );
};

export default TaskItem;
