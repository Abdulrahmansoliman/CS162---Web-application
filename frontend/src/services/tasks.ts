/**
 * Task/Todo service
 * Handles all CRUD operations for TodoLists and TodoItems
 */

import apiClient from './api';
import type {
  TodoList,
  TodoItem,
  CreateListData,
  UpdateListData,
  CreateItemData,
  UpdateItemData,
  MoveItemData,
} from '@/types';

export const taskService = {
  // ============================================================================
  // TodoList Operations
  // ============================================================================

  /**
   * Get all lists for current user
   */
  async getLists(): Promise<TodoList[]> {
    const response = await apiClient.get<TodoList[]>('/lists');
    return response.data;
  },

  /**
   * Get a specific list with all items (hierarchical)
   */
  async getList(listId: number): Promise<TodoList> {
    const response = await apiClient.get<TodoList>(`/lists/${listId}`);
    return response.data;
  },

  /**
   * Create a new list
   */
  async createList(data: CreateListData): Promise<TodoList> {
    const response = await apiClient.post<TodoList>('/lists', data);
    return response.data;
  },

  /**
   * Update a list
   */
  async updateList(listId: number, data: UpdateListData): Promise<TodoList> {
    const response = await apiClient.put<TodoList>(`/lists/${listId}`, data);
    return response.data;
  },

  /**
   * Delete a list
   */
  async deleteList(listId: number): Promise<void> {
    await apiClient.delete(`/lists/${listId}`);
  },

  // ============================================================================
  // TodoItem Operations
  // ============================================================================

  /**
   * Get a specific item
   */
  async getItem(itemId: number): Promise<TodoItem> {
    const response = await apiClient.get<TodoItem>(`/items/${itemId}`);
    return response.data;
  },

  /**
   * Create a new item (can be top-level or child)
   */
  async createItem(data: CreateItemData): Promise<TodoItem> {
    const response = await apiClient.post<TodoItem>('/items', data);
    return response.data;
  },

  /**
   * Update an item
   */
  async updateItem(itemId: number, data: UpdateItemData): Promise<TodoItem> {
    const response = await apiClient.put<TodoItem>(`/items/${itemId}`, data);
    return response.data;
  },

  /**
   * Delete an item (cascades to children)
   */
  async deleteItem(itemId: number): Promise<void> {
    await apiClient.delete(`/items/${itemId}`);
  },

  /**
   * Move item to a different list (top-level items only)
   */
  async moveItem(itemId: number, data: MoveItemData): Promise<TodoItem> {
    const response = await apiClient.patch<TodoItem>(`/items/${itemId}/move`, data);
    return response.data;
  },

  /**
   * Toggle item completion status
   */
  async toggleComplete(itemId: number, currentStatus: boolean): Promise<TodoItem> {
    return this.updateItem(itemId, { is_completed: !currentStatus });
  },

  /**
   * Toggle item collapsed status
   */
  async toggleCollapsed(itemId: number, currentStatus: boolean): Promise<TodoItem> {
    return this.updateItem(itemId, { is_collapsed: !currentStatus });
  },
};
