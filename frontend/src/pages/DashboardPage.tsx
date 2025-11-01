/**
 * Dashboard Page
 * Overview of all todo lists with beautiful grid layout
 */

import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { IoList, IoAdd, IoCheckmarkCircle, IoEllipsisVertical } from 'react-icons/io5';
import { useTasks } from '@/contexts/TaskContext';
import Card from '@/components/common/Card';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import Button from '@/components/common/Button';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { lists, fetchLists, isLoading } = useTasks();

  useEffect(() => {
    fetchLists();
  }, []);

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
            onClick={() => {/* Sidebar will handle this */}}
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
                className="p-6 hover:border-primary-300 border-2 border-transparent"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="bg-gradient-to-br from-primary-500 to-accent-500 p-2 rounded-lg">
                      <IoList size={24} className="text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 line-clamp-1">
                      {list.title}
                    </h3>
                  </div>
                  <button className="text-gray-400 hover:text-gray-600 p-1 rounded hover:bg-gray-100">
                    <IoEllipsisVertical size={20} />
                  </button>
                </div>

                {list.description && (
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                    {list.description}
                  </p>
                )}

                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <div className="flex items-center gap-1">
                    <IoCheckmarkCircle size={16} />
                    <span>0 tasks</span>
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
    </div>
  );
};

export default DashboardPage;
