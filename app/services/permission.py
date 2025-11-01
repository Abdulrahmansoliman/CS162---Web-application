"""
Authorization service module
Handles user permissions and data access control
"""

from models import User, TodoList, TodoItem
from flask import session


class PermissionService:
    """
    Permission service for access control.
    
    Verifies that users can only access their own data.
    Centralized permission checking prevents unauthorized access.
    """
    
    @staticmethod
    def get_current_user_id():
        """Get current authenticated user ID from session"""
        return session.get('user_id')
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        return session.get('user_id') is not None
    
    @staticmethod
    def owns_list(list_id):
        """
        Check if current user owns the list.
        
        Args:
            list_id: TodoList ID
            
        Returns:
            True if user owns list, False otherwise
        """
        user_id = PermissionService.get_current_user_id()
        
        if user_id is None:
            return False
        
        todo_list = TodoList.query.get(list_id)
        
        if todo_list is None:
            return False
        
        return todo_list.user_id == user_id
    
    @staticmethod
    def owns_item(item_id):
        """
        Check if current user owns the item.
        
        Args:
            item_id: TodoItem ID
            
        Returns:
            True if user owns item, False otherwise
        """
        user_id = PermissionService.get_current_user_id()
        
        if user_id is None:
            return False
        
        item = TodoItem.query.get(item_id)
        
        if item is None:
            return False
        
        # Item is owned by user if its list belongs to user
        todo_list = item.list
        
        return todo_list.user_id == user_id
    
    @staticmethod
    def get_user_lists():
        """
        Get all lists for current user.
        
        Returns:
            List of TodoList objects
        """
        user_id = PermissionService.get_current_user_id()
        
        if user_id is None:
            return []
        
        return TodoList.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_list_items(list_id):
        """
        Get all items for a list (if user owns list).
        
        Args:
            list_id: TodoList ID
            
        Returns:
            List of TodoItem objects or empty list if unauthorized
        """
        if not PermissionService.owns_list(list_id):
            return []
        
        # Get only top-level items (parent_id is NULL)
        return TodoItem.query.filter_by(
            list_id=list_id,
            parent_id=None
        ).order_by(TodoItem.order).all()
