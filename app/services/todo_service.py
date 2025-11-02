"""
Todo Service - Business Logic Layer

SINGLE RESPONSIBILITY PRINCIPLE (SRP):
This module has ONE responsibility: Implement todo business logic.
It does NOT handle:
  - HTTP requests/responses (that's routes' job)
  - Database schema (that's models' job)
  - Authentication (that's auth service's job)

ABSTRACTION PRINCIPLE:
Complex operations are hidden behind simple method calls.
Routes don't need to know HOW a task is created, just call create_item().

SEPARATION OF CONCERNS:
  - Routes: HTTP handling
  - Services: Business logic  ← YOU ARE HERE
  - Models: Data structure
  - Database: Persistence

BENEFITS:
1. REUSABILITY: Services can be used by routes, CLI tools, background jobs
2. TESTABILITY: Easy to unit test without HTTP layer
3. MAINTAINABILITY: Business logic changes stay in service layer
4. DRY (Don't Repeat Yourself): Shared logic isn't duplicated across routes

DESIGN PATTERNS USED:
  - Service Layer Pattern: Encapsulates business logic
  - Facade Pattern: Provides simplified interface to complex operations
"""

from models import db, TodoList, TodoItem
from typing import Optional, Dict, List, Any


class TodoListService:
    """
    Service for TodoList business logic.
    
    SINGLE RESPONSIBILITY: Manage todo list operations
    ABSTRACTION: Hides database operations from routes
    
    All methods are static because:
    1. No instance state is needed
    2. Can be called without instantiation
    3. Clear that methods don't modify service state
    """
    
    @staticmethod
    def create_list(user_id: int, title: str, description: Optional[str] = None) -> TodoList:
        """
        Create a new todo list.
        
        Args:
            user_id: Owner's user ID
            title: List title
            description: Optional description
            
        Returns:
            Created TodoList object
        """
        todo_list = TodoList(
            user_id=user_id,
            title=title,
            description=description
        )
        
        db.session.add(todo_list)
        db.session.commit()
        
        return todo_list
    
    @staticmethod
    def update_list(todo_list: TodoList, data: Dict[str, Any]) -> TodoList:
        """
        Update a todo list.
        
        Args:
            todo_list: TodoList object to update
            data: Dictionary with update fields
            
        Returns:
            Updated TodoList object
        """
        if 'title' in data:
            todo_list.title = data['title']
        
        if 'description' in data:
            todo_list.description = data['description']
        
        db.session.commit()
        
        return todo_list
    
    @staticmethod
    def delete_list(todo_list: TodoList) -> None:
        """
        Delete a todo list (cascades to all items).
        
        Args:
            todo_list: TodoList object to delete
        """
        db.session.delete(todo_list)
        db.session.commit()
    
    @staticmethod
    def complete_all_tasks(list_id: int) -> int:
        """
        Mark all tasks in a list as complete.
        
        Args:
            list_id: List ID
            
        Returns:
            Number of tasks marked complete
        """
        all_items = TodoItem.query.filter_by(list_id=list_id).all()
        
        count = 0
        for item in all_items:
            if not item.is_completed:
                item.is_completed = True
                count += 1
        
        db.session.commit()
        
        return count


class TodoItemService:
    """
    Service for TodoItem business logic.
    
    SINGLE RESPONSIBILITY PRINCIPLE:
    Handles ALL todo item operations in one place:
      - Creation, updates, deletion
      - Parent-child relationships
      - Completion chain management
      - Moving between lists/parents
    
    ABSTRACTION:
    Complex operations like "update item" involve:
      - Validation
      - Completion chain updates
      - Priority validation
      - Database commits
    All hidden behind simple method calls.
    
    ENCAPSULATION:
    Private helper methods (prefixed with _) hide implementation details.
    Public methods provide the clean interface routes need.
    """
    
    # CONSTANT: Valid priority levels
    # Using class constant demonstrates ENCAPSULATION
    # Changes to valid priorities only need to happen here
    VALID_PRIORITIES = ['low', 'medium', 'high', 'urgent']
    
    @staticmethod
    def validate_parent(parent_id: Optional[int], list_id: int) -> Optional[str]:
        """
        Validate parent item exists and belongs to same list.
        
        Args:
            parent_id: Parent item ID (can be None)
            list_id: List ID
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if parent_id is None:
            return None
        
        parent = TodoItem.query.get(parent_id)
        
        if parent is None:
            return 'Parent item not found'
        
        if parent.list_id != list_id:
            return 'Parent item not in same list'
        
        return None
    
    @staticmethod
    def create_item(
        list_id: int,
        title: str,
        parent_id: Optional[int] = None,
        description: Optional[str] = None,
        priority: str = 'medium',
        order: int = 0
    ) -> TodoItem:
        """
        Create a new todo item.
        
        Args:
            list_id: List ID
            title: Item title
            parent_id: Parent item ID (None for top-level)
            description: Optional description
            priority: Priority level
            order: Display order
            
        Returns:
            Created TodoItem object
        """
        item = TodoItem(
            list_id=list_id,
            parent_id=parent_id,
            title=title,
            description=description,
            priority=priority,
            order=order
        )
        
        db.session.add(item)
        
        # If adding a child to a completed parent, uncomplete the parent chain
        if parent_id is not None:
            parent = TodoItem.query.get(parent_id)
            if parent and parent.is_completed:
                parent.is_completed = False
                parent.uncomplete_parent_chain()
        
        db.session.commit()
        
        return item
    
    @staticmethod
    def update_item(item: TodoItem, data: Dict[str, Any]) -> tuple[Optional[TodoItem], Optional[str]]:
        """
        Update a todo item with validation.
        
        Args:
            item: TodoItem object to update
            data: Dictionary with update fields
            
        Returns:
            Tuple of (updated_item, error_message)
            If error_message is not None, update failed
        """
        # Update simple fields
        if 'title' in data:
            item.title = data['title']
        
        if 'description' in data:
            item.description = data['description']
        
        if 'order' in data:
            item.order = data['order']
        
        # Handle completion with validation
        if 'is_completed' in data:
            error = TodoItemService._handle_completion_update(item, data['is_completed'])
            if error:
                return None, error
        
        # Handle collapsed state
        if 'is_collapsed' in data:
            item.is_collapsed = data['is_collapsed']
        
        # Handle priority with validation
        if 'priority' in data:
            if data['priority'] not in TodoItemService.VALID_PRIORITIES:
                return None, f'Invalid priority. Must be one of: {", ".join(TodoItemService.VALID_PRIORITIES)}'
            item.priority = data['priority']
        
        db.session.commit()
        
        return item, None
    
    @staticmethod
    def _handle_completion_update(item: TodoItem, new_completed_state: bool) -> Optional[str]:
        """
        Handle completion state change with parent chain updates.
        
        Args:
            item: TodoItem to update
            new_completed_state: New completion state
            
        Returns:
            Error message if validation fails, None otherwise
        """
        # If trying to mark as completed, check if allowed
        if new_completed_state and not item.can_be_completed():
            return 'Cannot complete task: child tasks must be completed first'
        
        # If marking as uncompleted, propagate up to parents
        if not new_completed_state and item.is_completed:
            item.is_completed = False
            item.uncomplete_parent_chain()
        else:
            item.is_completed = new_completed_state
            # If marking as completed, auto-complete parent chain if possible
            if new_completed_state:
                item.auto_complete_parent_chain()
        
        return None
    
    @staticmethod
    def delete_item(item: TodoItem) -> None:
        """
        Delete a todo item (cascades to children).
        
        Args:
            item: TodoItem object to delete
        """
        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def move_to_list(item: TodoItem, target_list_id: int) -> Optional[str]:
        """
        Move a top-level item to a different list.
        
        Args:
            item: TodoItem to move
            target_list_id: Target list ID
            
        Returns:
            Error message if validation fails, None otherwise
        """
        # Only allow moving top-level items
        if item.parent_id is not None:
            return 'Can only move top-level items'
        
        item.list_id = target_list_id
        db.session.commit()
        
        return None
    
    @staticmethod
    def move_to_parent(item: TodoItem, new_parent_id: Optional[int]) -> Optional[str]:
        """
        Move an item to a new parent or root level.
        
        Args:
            item: TodoItem to move
            new_parent_id: New parent ID (None for root level)
            
        Returns:
            Error message if validation fails, None otherwise
        """
        # Validate new parent
        if new_parent_id is not None:
            new_parent = TodoItem.query.get(new_parent_id)
            
            if new_parent is None:
                return 'Parent item not found'
            
            if new_parent.list_id != item.list_id:
                return 'Cannot move to different list'
            
            # Prevent circular references
            if new_parent.id == item.id or item.is_ancestor_of(new_parent):
                return 'Cannot move to descendant'
        
        old_parent_id = item.parent_id
        
        # Only proceed if parent actually changed
        if old_parent_id == new_parent_id:
            return None
        
        item.parent_id = new_parent_id
        
        # Update order to end of new parent's children
        TodoItemService._update_item_order(item, new_parent_id)
        
        # Handle parent completion chains
        TodoItemService._handle_parent_chain_updates(old_parent_id, new_parent_id)
        
        db.session.commit()
        
        return None
    
    @staticmethod
    def _update_item_order(item: TodoItem, new_parent_id: Optional[int]) -> None:
        """
        Update item order when moving to new parent.
        
        Args:
            item: TodoItem being moved
            new_parent_id: New parent ID
        """
        if new_parent_id is None:
            # Moving to root - count root items
            max_order = db.session.query(
                db.func.max(TodoItem.order)
            ).filter(
                TodoItem.list_id == item.list_id,
                TodoItem.parent_id.is_(None)
            ).scalar() or 0
            item.order = max_order + 1
        else:
            # Moving under a parent - count that parent's children
            max_order = db.session.query(
                db.func.max(TodoItem.order)
            ).filter(
                TodoItem.parent_id == new_parent_id
            ).scalar() or 0
            item.order = max_order + 1
    
    @staticmethod
    def _handle_parent_chain_updates(old_parent_id: Optional[int], new_parent_id: Optional[int]) -> None:
        """
        Handle completion chain updates when moving items.
        
        Args:
            old_parent_id: Previous parent ID
            new_parent_id: New parent ID
        """
        # Uncomplete old parent chain if needed
        if old_parent_id is not None:
            old_parent = TodoItem.query.get(old_parent_id)
            if old_parent and old_parent.is_completed:
                old_parent.uncomplete_parent_chain()
        
        # Uncomplete new parent chain if needed
        if new_parent_id is not None:
            new_parent = TodoItem.query.get(new_parent_id)
            if new_parent and new_parent.is_completed:
                new_parent.uncomplete_parent_chain()
