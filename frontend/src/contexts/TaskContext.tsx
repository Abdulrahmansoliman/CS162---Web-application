/**
 * Task Context
 * Provides task/todo state and operations throughout the app
 * Manages lists and hierarchical items
 */

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { taskService } from '@/services/tasks';
import type {
  TodoList,
  TodoItem,
  CreateListData,
  UpdateListData,
  CreateItemData,
  UpdateItemData,
} from '@/types';
import toast from 'react-hot-toast';

interface TaskContextType {
  lists: TodoList[];
  currentList: TodoList | null;
  isLoading: boolean;
  
  // List operations
  fetchLists: () => Promise<void>;
  fetchList: (listId: number) => Promise<void>;
  createList: (data: CreateListData) => Promise<TodoList>;
  updateList: (listId: number, data: UpdateListData) => Promise<void>;
  deleteList: (listId: number) => Promise<void>;
  completeAllTasks: (listId: number) => Promise<void>;
  setCurrentList: (list: TodoList | null) => void;
  
  // Item operations
  createItem: (data: CreateItemData) => Promise<TodoItem>;
  updateItem: (itemId: number, data: UpdateItemData) => Promise<void>;
  deleteItem: (itemId: number) => Promise<void>;
  toggleComplete: (itemId: number, currentStatus: boolean) => Promise<void>;
  toggleCollapsed: (itemId: number, currentStatus: boolean) => Promise<void>;
  moveToParent: (itemId: number, newParentId: number | null) => Promise<void>;
  moveItemToList: (itemId: number, targetListId: number) => Promise<void>;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export const useTasks = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTasks must be used within TaskProvider');
  }
  return context;
};

interface TaskProviderProps {
  children: ReactNode;
}

export const TaskProvider: React.FC<TaskProviderProps> = ({ children }) => {
  const [lists, setLists] = useState<TodoList[]>([]);
  const [currentList, setCurrentListState] = useState<TodoList | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // ============================================================================
  // List Operations
  // ============================================================================

  const fetchLists = async () => {
    try {
      setIsLoading(true);
      const fetchedLists = await taskService.getLists();
      setLists(fetchedLists);
    } catch (error: any) {
      toast.error(error.message || 'Failed to fetch lists');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const fetchList = async (listId: number) => {
    try {
      setIsLoading(true);
      const list = await taskService.getList(listId);
      setCurrentListState(list);
      
      // Update in lists array as well
      setLists(prev => prev.map(l => l.id === listId ? list : l));
    } catch (error: any) {
      toast.error(error.message || 'Failed to fetch list');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const createList = async (data: CreateListData): Promise<TodoList> => {
    try {
      setIsLoading(true);
      const newList = await taskService.createList(data);
      setLists(prev => [...prev, newList]);
      toast.success('List created!');
      return newList;
    } catch (error: any) {
      toast.error(error.message || 'Failed to create list');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateList = async (listId: number, data: UpdateListData) => {
    try {
      setIsLoading(true);
      const updatedList = await taskService.updateList(listId, data);
      setLists(prev => prev.map(l => l.id === listId ? updatedList : l));
      if (currentList?.id === listId) {
        setCurrentListState(updatedList);
      }
      toast.success('List updated!');
    } catch (error: any) {
      toast.error(error.message || 'Failed to update list');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const deleteList = async (listId: number) => {
    try {
      setIsLoading(true);
      await taskService.deleteList(listId);
      setLists(prev => prev.filter(l => l.id !== listId));
      if (currentList?.id === listId) {
        setCurrentListState(null);
      }
      toast.success('List deleted');
    } catch (error: any) {
      toast.error(error.message || 'Failed to delete list');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const completeAllTasks = async (listId: number) => {
    try {
      setIsLoading(true);
      await taskService.completeAllTasks(listId);
      
      // Refresh the list to get updated counts and completion status
      await fetchList(listId);
      
      // Also refresh the lists array to update dashboard
      await fetchLists();
      
      toast.success('All tasks marked as complete!');
    } catch (error: any) {
      toast.error(error.message || 'Failed to complete all tasks');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const setCurrentList = (list: TodoList | null) => {
    setCurrentListState(list);
  };

  // ============================================================================
  // Item Operations
  // ============================================================================

  const createItem = async (data: CreateItemData): Promise<TodoItem> => {
    try {
      setIsLoading(true);
      const newItem = await taskService.createItem(data);
      
      // Refresh current list to get updated hierarchy
      if (currentList?.id === data.list_id) {
        await fetchList(data.list_id);
      }
      
      toast.success('Item created!');
      return newItem;
    } catch (error: any) {
      toast.error(error.message || 'Failed to create item');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateItem = async (itemId: number, data: UpdateItemData) => {
    try {
      setIsLoading(true);
      await taskService.updateItem(itemId, data);
      
      // Refresh current list to get updated data
      if (currentList) {
        await fetchList(currentList.id);
      }
      
      toast.success('Item updated!');
    } catch (error: any) {
      toast.error(error.message || 'Failed to update item');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const deleteItem = async (itemId: number) => {
    try {
      setIsLoading(true);
      await taskService.deleteItem(itemId);
      
      // Refresh current list to reflect deletion
      if (currentList) {
        await fetchList(currentList.id);
      }
      
      toast.success('Item deleted');
    } catch (error: any) {
      toast.error(error.message || 'Failed to delete item');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const toggleComplete = async (itemId: number, currentStatus: boolean) => {
    try {
      await taskService.toggleComplete(itemId, currentStatus);
      
      // Refresh current list
      if (currentList) {
        await fetchList(currentList.id);
      }
    } catch (error: any) {
      // Show specific error message from backend
      const errorMsg = error.response?.data?.error || error.message || 'Failed to toggle completion';
      toast.error(errorMsg);
      throw error;
    }
  };

  const toggleCollapsed = async (itemId: number, currentStatus: boolean) => {
    try {
      await taskService.toggleCollapsed(itemId, currentStatus);
      
      // Refresh current list
      if (currentList) {
        await fetchList(currentList.id);
      }
    } catch (error: any) {
      toast.error(error.message || 'Failed to toggle collapse');
      throw error;
    }
  };

  const moveToParent = async (itemId: number, newParentId: number | null) => {
    try {
      await taskService.moveToParent(itemId, newParentId);
      
      // Refresh current list to show new hierarchy
      if (currentList) {
        await fetchList(currentList.id);
      }
      toast.success('Task moved successfully');
    } catch (error: any) {
      const errorMsg = error.response?.data?.error || error.message || 'Failed to move task';
      toast.error(errorMsg);
      throw error;
    }
  };

  const moveItemToList = async (itemId: number, targetListId: number) => {
    try {
      await taskService.moveItem(itemId, { target_list_id: targetListId });
      
      // Refresh both lists and current list
      await fetchLists();
      if (currentList) {
        await fetchList(currentList.id);
      }
      toast.success('Task moved to new list');
    } catch (error: any) {
      const errorMsg = error.response?.data?.error || error.message || 'Failed to move task to list';
      toast.error(errorMsg);
      throw error;
    }
  };

  const value: TaskContextType = {
    lists,
    currentList,
    isLoading,
    fetchLists,
    fetchList,
    createList,
    updateList,
    deleteList,
    completeAllTasks,
    setCurrentList,
    createItem,
    updateItem,
    deleteItem,
    toggleComplete,
    toggleCollapsed,
    moveToParent,
    moveItemToList,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};
