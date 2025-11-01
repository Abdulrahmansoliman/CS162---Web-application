/**
 * List Page
 * Displays a single list with all its hierarchical items
 */

import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { IoArrowBack, IoAdd, IoTrash } from 'react-icons/io5';
import { useTasks } from '@/contexts/TaskContext';
import TaskItem from '@/components/tasks/TaskItem';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import Button from '@/components/common/Button';
import Modal from '@/components/common/Modal';
import Input from '@/components/common/Input';

const ListPage = () => {
  const { listId } = useParams<{ listId: string }>();
  const navigate = useNavigate();
  const { currentList, fetchList, createItem, deleteList, isLoading } = useTasks();
  const [showAddModal, setShowAddModal] = useState(false);
  const [newItemTitle, setNewItemTitle] = useState('');
  const [newItemDescription, setNewItemDescription] = useState('');

  useEffect(() => {
    if (listId) {
      fetchList(Number(listId));
    }
  }, [listId]);

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newItemTitle.trim() || !listId) return;

    try {
      await createItem({
        list_id: Number(listId),
        title: newItemTitle,
        description: newItemDescription || undefined,
      });
      setNewItemTitle('');
      setNewItemDescription('');
      setShowAddModal(false);
    } catch (error) {
      // Error handled by context
    }
  };

  const handleDeleteList = async () => {
    if (!listId) return;
    if (!confirm('Are you sure you want to delete this list? All tasks will be deleted.')) return;

    try {
      await deleteList(Number(listId));
      navigate('/dashboard');
    } catch (error) {
      // Error handled by context
    }
  };

  if (isLoading && !currentList) {
    return (
      <div className="flex items-center justify-center h-full">
        <LoadingSpinner size="large" message="Loading list..." />
      </div>
    );
  }

  if (!currentList) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-600 mb-4">List not found</p>
          <Button onClick={() => navigate('/dashboard')}>Go to Dashboard</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white border-b border-gray-200 px-4 md:px-8 py-6"
      >
        <div className="max-w-5xl mx-auto">
          <div className="flex items-center gap-4 mb-4">
            <Button
              onClick={() => navigate('/dashboard')}
              variant="ghost"
              icon={<IoArrowBack size={20} />}
            >
              Back
            </Button>
          </div>

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                {currentList.title}
              </h1>
              {currentList.description && (
                <p className="text-gray-600">{currentList.description}</p>
              )}
            </div>

            <div className="flex gap-2">
              <Button
                onClick={() => setShowAddModal(true)}
                variant="primary"
                icon={<IoAdd size={20} />}
              >
                Add Task
              </Button>
              <Button
                onClick={handleDeleteList}
                variant="danger"
                icon={<IoTrash size={20} />}
              >
                Delete List
              </Button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Tasks */}
      <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6">
        <div className="max-w-5xl mx-auto">
          {!currentList.items || currentList.items.length === 0 ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-16"
            >
              <div className="inline-block bg-gray-100 p-6 rounded-full mb-4">
                <IoAdd size={64} className="text-gray-400" />
              </div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">No tasks yet</h2>
              <p className="text-gray-600 mb-6">Add your first task to get started!</p>
              <Button
                onClick={() => setShowAddModal(true)}
                variant="primary"
                size="large"
                icon={<IoAdd size={20} />}
              >
                Add First Task
              </Button>
            </motion.div>
          ) : (
            <div className="space-y-2">
              {currentList.items.map((item) => (
                <TaskItem key={item.id} item={item} level={0} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Add Task Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Task"
        size="medium"
      >
        <form onSubmit={handleAddItem} className="space-y-4">
          <Input
            label="Task Title"
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
              Add Task
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default ListPage;
