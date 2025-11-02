/**
 * Dashboard Page
 * Overview of all todo lists with beautiful grid layout
 */

import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { IoList, IoAdd, IoCheckmarkCircle, IoEllipsisVertical, IoTrashOutline, IoCheckmarkDoneOutline } from 'react-icons/io5';
import { useTasks } from '@/contexts/TaskContext';
import Card from '@/components/common/Card';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import Button from '@/components/common/Button';
import Modal from '@/components/common/Modal';
import Input from '@/components/common/Input';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { lists, fetchLists, deleteList, completeAllTasks, createList, isLoading } = useTasks();
  const [openMenuId, setOpenMenuId] = useState<number | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showCompleteModal, setShowCompleteModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedListId, setSelectedListId] = useState<number | null>(null);
  const [newListTitle, setNewListTitle] = useState('');
  const [newListDescription, setNewListDescription] = useState('');

  useEffect(() => {
    fetchLists();
  }, []);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      if (openMenuId !== null) {
        setOpenMenuId(null);
      }
    };

    if (openMenuId !== null) {
      document.addEventListener('click', handleClickOutside);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [openMenuId]);

  const handleDeleteList = async () => {
    if (selectedListId === null) return;
    
    try {
      await deleteList(selectedListId);
      setShowDeleteModal(false);
      setSelectedListId(null);
    } catch (error) {
      console.error('Failed to delete list:', error);
    }
  };

  const handleCompleteAll = async () => {
    if (selectedListId === null) return;
    
    try {
      await completeAllTasks(selectedListId);
      setShowCompleteModal(false);
      setSelectedListId(null);
    } catch (error) {
      console.error('Failed to complete all tasks:', error);
    }
  };

  const handleCreateList = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newListTitle.trim()) return;

    try {
      await createList({
        title: newListTitle,
        description: newListDescription || undefined,
      });
      setNewListTitle('');
      setNewListDescription('');
      setShowCreateModal(false);
    } catch (error) {
      // Error handled by context
    }
  };

  const openDeleteModal = (listId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedListId(listId);
    setShowDeleteModal(true);
    setOpenMenuId(null);
  };

  const openCompleteModal = (listId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedListId(listId);
    setShowCompleteModal(true);
    setOpenMenuId(null);
  };

  const toggleMenu = (listId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    setOpenMenuId(openMenuId === listId ? null : listId);
  };

  const selectedList = lists.find(l => l.id === selectedListId);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 },
  };

  if (isLoading && lists.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <LoadingSpinner size="large" message="Loading your lists..." />
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
          Welcome to TaskFlow
        </h1>
        <p className="text-gray-600">Organize your life, one task at a time</p>
      </motion.div>

      {/* Lists Grid */}
      {lists.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center py-16"
        >
          <div className="inline-block bg-gray-100 p-6 rounded-full mb-4">
            <IoList size={64} className="text-gray-400" />
          </div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">No lists yet</h2>
          <p className="text-gray-600 mb-6">Create your first list to get started!</p>
          <Button
            onClick={() => setShowCreateModal(true)}
            variant="primary"
            size="large"
            icon={<IoAdd size={20} />}
          >
            Create Your First List
          </Button>
        </motion.div>
      ) : (
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {lists.map((list) => (
            <motion.div key={list.id} variants={item}>
              <Card
                onClick={() => navigate(`/list/${list.id}`)}
                className={`p-6 hover:border-primary-300 border-2 relative ${
                  list.all_completed 
                    ? 'border-green-300 bg-green-50/30' 
                    : 'border-transparent'
                }`}
              >
                {/* Three-dot menu */}
                <div className="absolute top-3 right-3 z-10">
                  <button
                    onClick={(e) => toggleMenu(list.id, e)}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    aria-label="List options"
                  >
                    <IoEllipsisVertical size={20} className="text-gray-600" />
                  </button>
                  
                  {/* Dropdown menu */}
                  <AnimatePresence>
                    {openMenuId === list.id && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: -10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: -10 }}
                        transition={{ duration: 0.15 }}
                        className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 py-1 z-20"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <button
                          onClick={(e) => openCompleteModal(list.id, e)}
                          className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-3 text-gray-700 transition-colors"
                          disabled={list.all_completed}
                        >
                          <IoCheckmarkDoneOutline size={18} className={list.all_completed ? 'text-gray-400' : 'text-green-500'} />
                          <span className={list.all_completed ? 'text-gray-400' : ''}>
                            {list.all_completed ? 'All tasks completed' : 'Mark all complete'}
                          </span>
                        </button>
                        <div className="border-t border-gray-100 my-1" />
                        <button
                          onClick={(e) => openDeleteModal(list.id, e)}
                          className="w-full px-4 py-2 text-left text-sm hover:bg-red-50 flex items-center gap-3 text-red-600 transition-colors"
                        >
                          <IoTrashOutline size={18} />
                          <span>Delete list</span>
                        </button>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

                {/* All Complete Badge */}
                {list.all_completed && (
                  <div className="absolute top-3 left-3 bg-green-500 text-white px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1 shadow-lg">
                    <IoCheckmarkCircle size={14} />
                    All Done!
                  </div>
                )}

                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${
                      list.all_completed
                        ? 'bg-gradient-to-br from-green-500 to-green-600'
                        : 'bg-gradient-to-br from-primary-500 to-accent-500'
                    }`}>
                      <IoList size={24} className="text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 line-clamp-1">
                      {list.title}
                    </h3>
                  </div>
                </div>

                {list.description && (
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                    {list.description}
                  </p>
                )}

                {/* Progress Bar */}
                <div className="mb-4">
                  <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <span>Progress</span>
                    <span className="font-medium">
                      {list.task_count > 0 
                        ? Math.round((list.completed_count / list.task_count) * 100)
                        : 0}%
                    </span>
                  </div>
                  <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ 
                        width: list.task_count > 0 
                          ? `${(list.completed_count / list.task_count) * 100}%` 
                          : '0%' 
                      }}
                      transition={{ duration: 0.5, ease: "easeOut" }}
                      className={`h-full rounded-full ${
                        list.all_completed
                          ? 'bg-gradient-to-r from-green-400 to-green-600'
                          : 'bg-gradient-to-r from-primary-400 to-accent-500'
                      }`}
                    />
                  </div>
                </div>

                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <div className="flex items-center gap-1">
                    <IoCheckmarkCircle size={16} className={list.all_completed ? 'text-green-500' : ''} />
                    <span className={list.all_completed ? 'text-green-600 font-medium' : ''}>
                      {list.completed_count}/{list.task_count} {list.task_count === 1 ? 'task' : 'tasks'}
                    </span>
                  </div>
                  <div className="text-xs">
                    {new Date(list.created_at).toLocaleDateString()}
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete List"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Are you sure you want to delete <span className="font-semibold">{selectedList?.title}</span>?
            This will permanently delete the list and all its tasks (including subtasks).
          </p>
          <div className="flex gap-3 justify-end">
            <Button
              variant="secondary"
              onClick={() => setShowDeleteModal(false)}
            >
              Cancel
            </Button>
            <Button
              variant="danger"
              onClick={handleDeleteList}
              icon={<IoTrashOutline size={18} />}
            >
              Delete List
            </Button>
          </div>
        </div>
      </Modal>

      {/* Complete All Confirmation Modal */}
      <Modal
        isOpen={showCompleteModal}
        onClose={() => setShowCompleteModal(false)}
        title="Mark All Tasks Complete"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            Are you sure you want to mark all tasks in <span className="font-semibold">{selectedList?.title}</span> as complete?
            This will mark all tasks and subtasks as done.
          </p>
          <div className="flex gap-3 justify-end">
            <Button
              variant="secondary"
              onClick={() => setShowCompleteModal(false)}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={handleCompleteAll}
              icon={<IoCheckmarkDoneOutline size={18} />}
            >
              Mark All Complete
            </Button>
          </div>
        </div>
      </Modal>

      {/* Create List Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New List"
        size="small"
      >
        <form onSubmit={handleCreateList} className="space-y-4">
          <Input
            label="List Title"
            placeholder="e.g., Shopping List"
            value={newListTitle}
            onChange={(e) => setNewListTitle(e.target.value)}
            autoFocus
          />
          <Input
            label="Description (optional)"
            placeholder="What's this list for?"
            value={newListDescription}
            onChange={(e) => setNewListDescription(e.target.value)}
          />
          <div className="flex gap-3">
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={() => setShowCreateModal(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              fullWidth
              disabled={!newListTitle.trim()}
            >
              Create
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default DashboardPage;
