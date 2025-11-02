"""
Authorization Service Module

SINGLE RESPONSIBILITY PRINCIPLE (SRP):
This module has ONE job: Handle authorization (who can access what).
It does NOT handle:
  - Authentication (that's auth.py)
  - Business logic (that's todo_service.py)
  - HTTP handling (that's routes)

ABSTRACTION:
Routes call simple methods like owns_list() or owns_item().
They don't need to know HOW permission checking works internally.

CENTRALIZATION:
All permission logic is in ONE place.
If permission rules change, we only update this file.

SECURITY:
Every route checks permissions using this service.
Prevents unauthorized data access.
"""

from models import User, TodoList, TodoItem
from flask import session


class PermissionService:
    """
    Permission service for access control.
    
    DESIGN PATTERN: Facade Pattern
    Provides a simple interface to complex permission checking logic.
    
    STATIC METHODS:
    All methods are static because:
    1. No instance state needed
    2. Can be called without instantiation: PermissionService.owns_list()
    3. Clear that methods don't modify service state
    
    SINGLE RESPONSIBILITY:
    This class ONLY checks permissions. It doesn't:
      - Create/update/delete data
      - Authenticate users
      - Handle HTTP requests
    """
    
    @staticmethod
    def get_current_user_id():
        """
        Get current authenticated user ID from session.
        
        ABSTRACTION:
        Hides session implementation details.
        If we switch from session to JWT, only this method changes.
        
        Returns:
            User ID if authenticated, None otherwise
        """
        return session.get('user_id')
    
    @staticmethod
    def is_authenticated():
        """
        Check if a user is currently authenticated.
        
        ENCAPSULATION:
        Simple yes/no answer. Caller doesn't need to know
        how we determine authentication status.
        
        Returns:
            True if user is logged in, False otherwise
        """
        return session.get('user_id') is not None
    
    @staticmethod
    def owns_list(list_id):
        """
        Check if current user owns the specified list.
        
        SECURITY:
        Critical for preventing unauthorized access.
        Every route that accesses a list MUST call this.
        
        ABSTRACTION:
        Hides the complexity of checking ownership:
          1. Get current user ID
          2. Fetch list from database
          3. Compare user IDs
        
        Args:
            list_id: TodoList ID to check
            
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
        
        INDIRECT OWNERSHIP:
        User owns an item if they own the list containing it.
        This demonstrates TRANSITIVE OWNERSHIP checking.
        
        SECURITY:
        Every route that accesses an item MUST call this.
        Prevents users from accessing other users' tasks.
        
        ABSTRACTION:
        Hides the complexity of:
          1. Getting current user
          2. Finding the item
          3. Finding the item's list
          4. Comparing ownership
        
        Args:
            item_id: TodoItem ID
            
        Returns:
            True if user owns item (via list ownership), False otherwise
        """
        user_id = PermissionService.get_current_user_id()
        
        if user_id is None:
            return False
        
        item = TodoItem.query.get(item_id)
        
        if item is None:
            return False
        
        # RELATIONSHIP NAVIGATION:
        # Item -> List -> User
        # Uses SQLAlchemy relationship defined in models
        todo_list = item.list
        
        return todo_list.user_id == user_id
    
    @staticmethod
    def get_user_lists():
        """
        Get all lists owned by current user.
        
        DATA FILTERING:
        Automatically filters to only user's data.
        Prevents accidental data leakage.
        
        ABSTRACTION:
        Simple method call hides database query complexity.
        
        Returns:
            List of TodoList objects owned by current user,
            or empty list if not authenticated
        """
        user_id = PermissionService.get_current_user_id()
        
        if user_id is None:
            return []
        
        # DATABASE QUERY with automatic filtering
        return TodoList.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_list_items(list_id):
        """
        Get all items for a list (if user owns list).
        
        SECURITY FIRST:
        Checks ownership BEFORE returning data.
        Fail-safe: Returns empty list if unauthorized.
        
        HIERARCHICAL DATA:
        Returns only TOP-LEVEL items (parent_id = NULL).
        Child items are accessed via parent.children relationship.
        
        ABSTRACTION:
        Combines permission check + data retrieval + sorting
        into one simple method call.
        
        Args:
            list_id: TodoList ID to fetch items from
            
        Returns:
            List of top-level TodoItem objects ordered by 'order' field,
            or empty list if unauthorized or list doesn't exist
        """
        # PERMISSION CHECK FIRST - fail-safe security
        if not PermissionService.owns_list(list_id):
            return []
        
        # SAFE TO QUERY: User owns this list
        # Get only top-level items (parent_id is NULL)
        return TodoItem.query.filter_by(
            list_id=list_id,
            parent_id=None
        ).order_by(TodoItem.order).all()
