"""
Todo List and Item Routes

ARCHITECTURE OVERVIEW:
This module demonstrates the LAYERED ARCHITECTURE pattern:
  - Routes Layer (this file): HTTP request/response handling
  - Service Layer (todo_service.py): Business logic
  - Data Layer (models): Database operations

SINGLE RESPONSIBILITY PRINCIPLE (SRP):
Each route function has ONE job: Handle an HTTP endpoint
  - Parse request data
  - Validate authentication/authorization
  - Delegate to service layer
  - Format response

ABSTRACTION:
Routes don't know HOW tasks are created, updated, or deleted.
They just call service methods and trust the service layer to handle it.

BENEFITS OF THIS ARCHITECTURE:
1. Testability: Service layer can be unit tested independently
2. Reusability: Services can be used by other routes or background jobs
3. Maintainability: Business logic changes don't require route changes
4. Separation of Concerns: HTTP logic ≠ business logic
"""

from flask import Blueprint, request
from models import TodoList, TodoItem
from app.services import (
    PermissionService,
    TodoListService,
    TodoItemService
)

todo_bp = Blueprint('todo', __name__)


# ============================================================================
# TodoList Routes
# Routes for managing todo lists (create, read, update, delete)
# ============================================================================

@todo_bp.route('/lists', methods=['POST'])
def create_list():
    """
    Create a new todo list for current user.
    
    Expected JSON:
        {
            "title": "string",
            "description": "string (optional)"
        }
    
    Returns:
        Success: {"id": int, "title": "string", ...}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return {'error': 'Missing required field: title'}, 400
    
    user_id = PermissionService.get_current_user_id()
    
    todo_list = TodoListService.create_list(
        user_id=user_id,
        title=data['title'],
        description=data.get('description')
    )
    
    return todo_list.to_dict(), 201


@todo_bp.route('/lists', methods=['GET'])
def get_lists():
    """
    Get all todo lists for current user.
    
    Returns:
        Success: [{"id": int, "title": "string", ...}]
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    lists = PermissionService.get_user_lists()
    
    return [lst.to_dict() for lst in lists], 200


@todo_bp.route('/lists/<int:list_id>', methods=['GET'])
def get_list(list_id):
    """
    Get a specific todo list with all items (hierarchical).
    
    Returns:
        Success: {"id": int, "title": "string", "items": [...]}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_list(list_id):
        return {'error': 'Unauthorized'}, 403
    
    todo_list = TodoList.query.get(list_id)
    
    if todo_list is None:
        return {'error': 'List not found'}, 404
    
    return todo_list.to_dict(include_items=True), 200


@todo_bp.route('/lists/<int:list_id>', methods=['PUT'])
def update_list(list_id):
    """
    Update a todo list.
    
    Expected JSON:
        {
            "title": "string (optional)",
            "description": "string (optional)"
        }
    
    Returns:
        Success: {"id": int, ...}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_list(list_id):
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    if not data:
        return {'error': 'No JSON data provided'}, 400
    
    todo_list = TodoList.query.get(list_id)
    
    if todo_list is None:
        return {'error': 'List not found'}, 404
    
    updated_list = TodoListService.update_list(todo_list, data)
    
    return updated_list.to_dict(), 200


@todo_bp.route('/lists/<int:list_id>', methods=['DELETE'])
def delete_list(list_id):
    """
    Delete a todo list and all its items (cascading delete).
    
    Returns:
        Success: {"message": "List deleted"}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_list(list_id):
        return {'error': 'Unauthorized'}, 403
    
    todo_list = TodoList.query.get(list_id)
    
    if todo_list is None:
        return {'error': 'List not found'}, 404
    
    TodoListService.delete_list(todo_list)
    
    return {'message': 'List deleted'}, 200


@todo_bp.route('/lists/<int:list_id>/complete-all', methods=['PATCH'])
def complete_all_tasks(list_id):
    """
    Mark all tasks and subtasks in a list as complete.
    
    Returns:
        Success: {"message": "All tasks marked as complete", "count": int}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_list(list_id):
        return {'error': 'Unauthorized'}, 403
    
    todo_list = TodoList.query.get(list_id)
    
    if todo_list is None:
        return {'error': 'List not found'}, 404
    
    count = TodoListService.complete_all_tasks(list_id)
    
    return {
        'message': 'All tasks marked as complete',
        'count': count
    }, 200


# ============================================================================
# TodoItem Routes
# ============================================================================

@todo_bp.route('/items', methods=['POST'])
def create_item():
    """
    Create a new todo item or sub-item.
    
    Expected JSON:
        {
            "list_id": int,
            "parent_id": int (optional, null for top-level),
            "title": "string",
            "description": "string (optional)",
            "order": int (optional, default 0)
        }
    
    Returns:
        Success: {"id": int, "title": "string", ...}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    data = request.get_json()
    
    if not data:
        return {'error': 'No JSON data provided'}, 400
    
    # Validate required fields
    list_id = data.get('list_id')
    title = data.get('title')
    
    if not list_id or not title:
        return {'error': 'Missing required fields: list_id, title'}, 400
    
    # Check user owns the list
    if not PermissionService.owns_list(list_id):
        return {'error': 'Unauthorized'}, 403
    
    # Validate parent if provided
    parent_id = data.get('parent_id')
    error = TodoItemService.validate_parent(parent_id, list_id)
    if error:
        return {'error': error}, 400
    
    # Create item using service
    item = TodoItemService.create_item(
        list_id=list_id,
        title=title,
        parent_id=parent_id,
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        order=data.get('order', 0)
    )
    
    return item.to_dict(), 201


@todo_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Get a specific item with all its children (recursive).
    
    Returns:
        Success: {"id": int, "title": "string", "children": [...]}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_item(item_id):
        return {'error': 'Unauthorized'}, 403
    
    item = TodoItem.query.get(item_id)
    
    if item is None:
        return {'error': 'Item not found'}, 404
    
    return item.to_dict(include_children=True), 200


@todo_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Update a todo item.
    
    Expected JSON:
        {
            "title": "string (optional)",
            "description": "string (optional)",
            "is_completed": bool (optional),
            "is_collapsed": bool (optional)",
            "order": int (optional)
        }
    
    Returns:
        Success: {"id": int, ...}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_item(item_id):
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    if not data:
        return {'error': 'No JSON data provided'}, 400
    
    item = TodoItem.query.get(item_id)
    
    if item is None:
        return {'error': 'Item not found'}, 404
    
    # Update using service
    updated_item, error = TodoItemService.update_item(item, data)
    
    if error:
        return {'error': error}, 400
    
    return updated_item.to_dict(), 200


@todo_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Delete a todo item and all its descendants (cascading delete).
    
    Returns:
        Success: {"message": "Item deleted"}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_item(item_id):
        return {'error': 'Unauthorized'}, 403
    
    item = TodoItem.query.get(item_id)
    
    if item is None:
        return {'error': 'Item not found'}, 404
    
    TodoItemService.delete_item(item)
    
    return {'message': 'Item deleted'}, 200


@todo_bp.route('/items/<int:item_id>/move', methods=['PATCH'])
def move_item(item_id):
    """
    Move a top-level item to a different list.
    
    Only top-level items (parent_id = NULL) can be moved to other lists.
    
    Expected JSON:
        {
            "target_list_id": int
        }
    
    Returns:
        Success: {"id": int, ...}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_item(item_id):
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    if not data or 'target_list_id' not in data:
        return {'error': 'Missing required field: target_list_id'}, 400
    
    item = TodoItem.query.get(item_id)
    
    if item is None:
        return {'error': 'Item not found'}, 404
    
    target_list_id = data['target_list_id']
    
    # Verify user owns target list
    if not PermissionService.owns_list(target_list_id):
        return {'error': 'Target list not found or unauthorized'}, 404
    
    # Move item using service
    error = TodoItemService.move_to_list(item, target_list_id)
    if error:
        return {'error': error}, 400
    
    return item.to_dict(), 200


@todo_bp.route('/items/<int:item_id>/move-to-parent', methods=['PATCH'])
def move_item_to_parent(item_id):
    """
    Move a todo item to a new parent (or to root level).
    
    Expected JSON:
        {
            "new_parent_id": int or null  # New parent (null for top-level)
        }
    
    Returns:
        Success: {"id": int, ...}
        Error: {"error": "string"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    if not PermissionService.owns_item(item_id):
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    if data is None:
        return {'error': 'Missing request body'}, 400
    
    item = TodoItem.query.get(item_id)
    
    if item is None:
        return {'error': 'Item not found'}, 404
    
    new_parent_id = data.get('new_parent_id')
    
    # Move item using service
    error = TodoItemService.move_to_parent(item, new_parent_id)
    if error:
        return {'error': error}, 400
    
    return item.to_dict(), 200
