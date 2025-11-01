/**
 * Sidebar Component
 * Navigation sidebar with list of todo lists
 */

import { motion, AnimatePresence } from 'framer-motion';
import { IoAdd, IoList, IoClose } from 'react-icons/io5';
import { Link, useParams } from 'react-router-dom';
import { useTasks } from '@/contexts/TaskContext';
import { useEffect, useState } from 'react';
import Button from '../common/Button';
import Modal from '../common/Modal';
import Input from '../common/Input';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { lists, fetchLists, createList, isLoading } = useTasks();
  const { listId } = useParams();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newListTitle, setNewListTitle] = useState('');
  const [newListDescription, setNewListDescription] = useState('');

  useEffect(() => {
    fetchLists();
  }, []);

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

  const sidebarContent = (
    <div className="h-full flex flex-col bg-white border-r border-gray-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">My Lists</h2>
        <button
          onClick={onClose}
          className="lg:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <IoClose size={24} />
        </button>
      </div>

      {/* New List Button */}
      <div className="p-4">
        <Button
          onClick={() => setShowCreateModal(true)}
          variant="primary"
          fullWidth
          icon={<IoAdd size={20} />}
        >
          New List
        </Button>
      </div>

      {/* Lists */}
      <div className="flex-1 overflow-y-auto px-2">
        {isLoading && lists.length === 0 ? (
          <div className="text-center py-8 text-gray-500 text-sm">Loading...</div>
        ) : lists.length === 0 ? (
          <div className="text-center py-8 text-gray-500 text-sm">
            <IoList size={48} className="mx-auto mb-2 opacity-50" />
            <p>No lists yet</p>
            <p className="text-xs mt-1">Create your first list!</p>
          </div>
        ) : (
          <div className="space-y-1">
            {lists.map((list) => (
              <Link
                key={list.id}
                to={`/list/${list.id}`}
                onClick={() => onClose()}
                className={`
                  block px-4 py-3 rounded-lg transition-all duration-200
                  ${
                    String(list.id) === listId
                      ? 'bg-primary-100 text-primary-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-100'
                  }
                `}
              >
                <div className="flex items-center gap-3">
                  <IoList size={20} />
                  <div className="flex-1 min-w-0">
                    <p className="truncate">{list.title}</p>
                    {list.description && (
                      <p className="text-xs opacity-70 truncate">{list.description}</p>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <div className="hidden lg:block w-64 h-screen sticky top-0">
        {sidebarContent}
      </div>

      {/* Mobile Sidebar */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onClose}
              className="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            />

            {/* Sidebar */}
            <motion.div
              initial={{ x: -280 }}
              animate={{ x: 0 }}
              exit={{ x: -280 }}
              transition={{ type: 'spring', damping: 25 }}
              className="lg:hidden fixed left-0 top-0 bottom-0 w-64 z-50"
            >
              {sidebarContent}
            </motion.div>
          </>
        )}
      </AnimatePresence>

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
    </>
  );
};

export default Sidebar;
