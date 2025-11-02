/**
 * useTaskItemLogic Custom Hook
 * 
 * SINGLE RESPONSIBILITY PRINCIPLE:
 * This hook's ONE responsibility is managing task item business logic and state.
 * It doesn't render UI - that's the component's job.
 * 
 * ABSTRACTION PRINCIPLE:
 * Abstracts complex state management and API interactions into a simple hook interface.
 * Components using this hook don't need to know HOW tasks are updated,
 * just WHAT operations are available.
 * 
 * SEPARATION OF CONCERNS:
 * - This hook: State + Logic
 * - TaskItem component: UI rendering
 * - TaskContext: Global state + API calls
 * 
 * REUSABILITY:
 * This hook can be used by any component that needs task item logic,
 * not just TaskItem.tsx
 */

import { useState } from 'react';
import { useTasks } from '@/contexts/TaskContext';
import { TodoItem } from '@/types';
import { getNextPriority } from './taskUtils';

/**
 * Custom hook for managing task item state and operations
 * 
 * Encapsulates:
 * - Modal visibility state
 * - Form field state (title, description, priority)
 * - All task operations (complete, edit, delete, move, etc.)
 * 
 * @param item - The task item being managed
 * @returns Object with state values and operation handlers
 */
export const useTaskItemLogic = (item: TodoItem) => {
  const { 
    lists, 
    toggleComplete, 
    toggleCollapsed, 
    createItem, 
    updateItem, 
    deleteItem, 
    moveItemToList 
  } = useTasks();

  // ========================================
  // STATE MANAGEMENT
  // ========================================

  // Modal visibility state
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showMoveModal, setShowMoveModal] = useState(false);

  // Add Child form state
  const [newItemTitle, setNewItemTitle] = useState('');
  const [newItemDescription, setNewItemDescription] = useState('');
  const [newItemPriority, setNewItemPriority] = useState<TodoItem['priority']>('medium');

  // Edit form state
  const [editTitle, setEditTitle] = useState(item.title);
  const [editDescription, setEditDescription] = useState(item.description || '');
  const [editPriority, setEditPriority] = useState(item.priority);

  // Move to list form state
  const [selectedListId, setSelectedListId] = useState<number | null>(null);

  // ========================================
  // COMPUTED VALUES
  // ========================================

  const hasChildren = item.children && item.children.length > 0;
  const canAddChild = true; // Infinite nesting enabled

  // ========================================
  // EVENT HANDLERS
  // ========================================

  /**
   * Toggle task completion status
   * 
   * ABSTRACTION: Simple interface hides API complexity
   */
  const handleToggleComplete = async () => {
    await toggleComplete(item.id, item.is_completed);
  };

  /**
   * Toggle task collapsed state (show/hide children)
   * 
   * Only called when task has children
   */
  const handleToggleCollapsed = async () => {
    if (hasChildren) {
      await toggleCollapsed(item.id, item.is_collapsed);
    }
  };

  /**
   * Add a child task
   * 
   * BUSINESS LOGIC:
   * 1. Validates title is not empty
   * 2. Creates child with current item as parent
   * 3. Resets form and closes modal
   */
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
      
      // Reset form
      setNewItemTitle('');
      setNewItemDescription('');
      setNewItemPriority('medium');
      setShowAddModal(false);
    } catch (error) {
      console.error('Failed to add child:', error);
    }
  };

  /**
   * Edit task details
   * 
   * BUSINESS LOGIC:
   * 1. Validates title is not empty
   * 2. Updates task via API
   * 3. Closes modal on success
   */
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
      console.error('Failed to edit item:', error);
    }
  };

  /**
   * Delete task
   * 
   * CASCADE BEHAVIOR:
   * Deleting a parent automatically deletes all children (database cascade)
   */
  const handleDelete = async () => {
    await deleteItem(item.id);
  };

  /**
   * Move task to a different list
   * 
   * BUSINESS RULE:
   * Only top-level tasks (level 0) can be moved between lists
   */
  const handleMoveToList = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedListId) return;

    try {
      await moveItemToList(item.id, selectedListId);
      setShowMoveModal(false);
      setSelectedListId(null);
    } catch (error) {
      console.error('Failed to move task:', error);
    }
  };

  /**
   * Cycle to next priority level
   * 
   * ABSTRACTION: Uses utility function to determine next priority
   */
  const handlePriorityCycle = async () => {
    const nextPriority = getNextPriority(item.priority);
    await updateItem(item.id, { priority: nextPriority });
  };

  /**
   * Open edit modal
   * 
   * Initializes form fields with current task values
   */
  const openEditModal = () => {
    setEditTitle(item.title);
    setEditDescription(item.description || '');
    setEditPriority(item.priority);
    setShowEditModal(true);
  };

  // ========================================
  // RETURN HOOK INTERFACE
  // ========================================

  return {
    // State
    showAddModal,
    showEditModal,
    showMoveModal,
    newItemTitle,
    newItemDescription,
    newItemPriority,
    editTitle,
    editDescription,
    editPriority,
    selectedListId,
    hasChildren,
    canAddChild,
    lists,

    // State setters
    setShowAddModal,
    setShowEditModal,
    setShowMoveModal,
    setNewItemTitle,
    setNewItemDescription,
    setNewItemPriority,
    setEditTitle,
    setEditDescription,
    setEditPriority,
    setSelectedListId,

    // Handlers
    handleToggleComplete,
    handleToggleCollapsed,
    handleAddChild,
    handleEdit,
    handleDelete,
    handleMoveToList,
    handlePriorityCycle,
    openEditModal,
  };
};
