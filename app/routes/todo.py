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
    
    # Get all items in the list (including nested)
    all_items = TodoItem.query.filter_by(list_id=list_id).all()
    
    # Mark all as complete
    count = 0
    for item in all_items:
        if not item.is_completed:
            item.is_completed = True
            count += 1
    
    db.session.commit()
    
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
    
    if parent_id is not None:
        parent = TodoItem.query.get(parent_id)
        
        if parent is None:
            return {'error': 'Parent item not found'}, 404
        
        # Check parent belongs to same list
        if parent.list_id != list_id:
            return {'error': 'Parent item not in same list'}, 400
        
        # Infinite nesting is now allowed
        # No depth check needed
    
    # Create item
    item = TodoItem(
        list_id=list_id,
        parent_id=parent_id,
        title=title,
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        order=data.get('order', 0)
    )
    
    db.session.add(item)
    
    # If adding a child to a completed parent, uncomplete the parent chain
    if parent_id is not None:
        parent = TodoItem.query.get(parent_id)
        if parent and parent.is_completed:
            parent.is_completed = False
            parent.uncomplete_parent_chain()
    
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
        new_completed_state = data['is_completed']
        
        # If trying to mark as completed, check if allowed
        if new_completed_state and not item.can_be_completed():
            return {
                'error': 'Cannot complete task: child tasks must be completed first'
            }, 400
        
        # If marking as uncompleted, propagate up to parents
        if not new_completed_state and item.is_completed:
            item.is_completed = False
            item.uncomplete_parent_chain()
        else:
            item.is_completed = new_completed_state
            # If marking as completed, auto-complete parent chain if possible
            if new_completed_state:
                item.auto_complete_parent_chain()
    
    if 'is_collapsed' in data:
        item.is_collapsed = data['is_collapsed']
    
    if 'order' in data:
        item.order = data['order']
    
    if 'priority' in data:
        # Validate priority value
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if data['priority'] in valid_priorities:
            item.priority = data['priority']
        else:
            return {
                'error': f'Invalid priority. Must be one of: {", ".join(valid_priorities)}'
            }, 400
    
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


@todo_bp.route('/items/<int:item_id>/move-to-parent', methods=['PATCH'])
def move_item_to_parent(item_id):
    """
    Move a todo item to a new parent (or to root level).
    Simplified approach - just changes the parent, order is auto-managed.
    
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
    
    # Validate new parent exists and belongs to same list
    if new_parent_id is not None:
        new_parent = TodoItem.query.get(new_parent_id)
        if new_parent is None:
            return {'error': 'Parent item not found'}, 404
        if new_parent.list_id != item.list_id:
            return {'error': 'Cannot move to different list'}, 400
        # Prevent moving item to be its own descendant
        if new_parent.id == item.id or item.is_ancestor_of(new_parent):
            return {'error': 'Cannot move to descendant'}, 400
    
    # Update parent
    old_parent_id = item.parent_id
    
    # Only proceed if parent actually changed
    if old_parent_id != new_parent_id:
        item.parent_id = new_parent_id
        
        # Set order to end of new parent's children
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
        
        # If parent changed, uncomplete the old parent chain
        if old_parent_id is not None:
            old_parent = TodoItem.query.get(old_parent_id)
            if old_parent and old_parent.is_completed:
                old_parent.uncomplete_parent_chain()
        
        # If moved to a completed parent, uncomplete the new parent chain
        if new_parent_id is not None:
            new_parent = TodoItem.query.get(new_parent_id)
            if new_parent and new_parent.is_completed:
                new_parent.uncomplete_parent_chain()
        
        db.session.commit()
    
    return item.to_dict(), 200
