"""
Todo list and item routes
Handles CRUD operations for lists and items with permission checks
"""

from flask import Blueprint, request
from models import db, TodoList, TodoItem
from app.services import PermissionService

todo_bp = Blueprint('todo', __name__)


# ============================================================================
# TodoList Routes
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
    
    todo_list = TodoList(
        user_id=user_id,
        title=data['title'],
        description=data.get('description')
    )
    
    db.session.add(todo_list)
    db.session.commit()
    
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
    
    if 'title' in data:
        todo_list.title = data['title']
    
    if 'description' in data:
        todo_list.description = data['description']
    
    db.session.commit()
    
    return todo_list.to_dict(), 200


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
    
    db.session.delete(todo_list)
    db.session.commit()
    
    return {'message': 'List deleted'}, 200


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
    
    if parent_id is not None:
        parent = TodoItem.query.get(parent_id)
        
        if parent is None:
            return {'error': 'Parent item not found'}, 404
        
        # Check parent belongs to same list
        if parent.list_id != list_id:
            return {'error': 'Parent item not in same list'}, 400
        
        # Check max depth (3 levels)
        if not parent.can_add_child():
            return {
                'error': 'Maximum nesting depth (3 levels) reached'
            }, 400
    
    # Create item
    item = TodoItem(
        list_id=list_id,
        parent_id=parent_id,
        title=title,
        description=data.get('description'),
        order=data.get('order', 0)
    )
    
    db.session.add(item)
    db.session.commit()
    
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
    
    # Update fields
    if 'title' in data:
        item.title = data['title']
    
    if 'description' in data:
        item.description = data['description']
    
    if 'is_completed' in data:
        item.is_completed = data['is_completed']
    
    if 'is_collapsed' in data:
        item.is_collapsed = data['is_collapsed']
    
    if 'order' in data:
        item.order = data['order']
    
    db.session.commit()
    
    return item.to_dict(), 200


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
    
    db.session.delete(item)
    db.session.commit()
    
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
    
    # Only allow moving top-level items
    if item.parent_id is not None:
        return {'error': 'Can only move top-level items'}, 400
    
    target_list_id = data['target_list_id']
    
    # Verify user owns target list
    if not PermissionService.owns_list(target_list_id):
        return {'error': 'Target list not found or unauthorized'}, 404
    
    # Move item
    item.list_id = target_list_id
    db.session.commit()
    
    return item.to_dict(), 200
