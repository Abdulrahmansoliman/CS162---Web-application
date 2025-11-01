/**
 * Type definitions for the Hierarchical Todo Application
 */

// User types
export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  user_id: number;
  username: string;
}

// TodoList types
export interface TodoList {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  items?: TodoItem[];
}

export interface CreateListData {
  title: string;
  description?: string;
}

export interface UpdateListData {
  title?: string;
  description?: string;
}

// TodoItem types (Hierarchical)
export interface TodoItem {
  id: number;
  list_id: number;
  parent_id: number | null;
  title: string;
  description: string | null;
  is_completed: boolean;
  is_collapsed: boolean;
  order: number;
  created_at: string;
  updated_at: string;
  children?: TodoItem[];
}

export interface CreateItemData {
  list_id: number;
  parent_id?: number | null;
  title: string;
  description?: string;
  order?: number;
}

export interface UpdateItemData {
  title?: string;
  description?: string;
  is_completed?: boolean;
  is_collapsed?: boolean;
  order?: number;
}

export interface MoveItemData {
  new_list_id: number;
}

// API Response types
export interface ApiError {
  error: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// UI State types
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface TaskState {
  lists: TodoList[];
  currentList: TodoList | null;
  isLoading: boolean;
  error: string | null;
}
