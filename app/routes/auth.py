"""
Authentication routes
Handles user registration, login, and logout endpoints
"""

from flask import Blueprint, request
from app.services import auth_service, PermissionService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    
    Returns:
        Success: {"user_id": int, "username": "string"}
        Error: {"error": "string"}
    """
    data = request.get_json()
    
    if not data:
        return {'error': 'No JSON data provided'}, 400
    
    # Validate required fields
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return {
            'error': 'Missing required fields: username, email, password'
        }, 400
    
    # Validate input lengths
    if len(username) < 3 or len(username) > 80:
        return {'error': 'Username must be 3-80 characters'}, 400
    
    if len(password) < 6:
        return {'error': 'Password must be at least 6 characters'}, 400
    
    # Register user
    user = auth_service.register_user(username, email, password)
    
    if user is None:
        return {
            'error': 'Username or email already exists'
        }, 409
    
    # Create session for new user
    auth_service.create_session(user)
    
    return {
        'user_id': user.id,
        'username': user.username
    }, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login with username and password.
    
    Expected JSON:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        Success: {"user_id": int, "username": "string"}
        Error: {"error": "string"}
    """
    data = request.get_json()
    
    if not data:
        return {'error': 'No JSON data provided'}, 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return {
            'error': 'Missing required fields: username, password'
        }, 400
    
    # Authenticate user
    user = auth_service.authenticate(username=username, password=password)
    
    if user is None:
        return {'error': 'Invalid username or password'}, 401
    
    # Create session
    auth_service.create_session(user)
    
    return {
        'user_id': user.id,
        'username': user.username
    }, 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    User logout.
    
    Returns:
        Success: {"message": "Logged out"}
    """
    auth_service.destroy_session()
    
    return {'message': 'Logged out'}, 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Get current authenticated user information.
    
    Returns:
        Success: {"user_id": int, "username": "string", "email": "string"}
        Error: {"error": "Not authenticated"}
    """
    if not PermissionService.is_authenticated():
        return {'error': 'Not authenticated'}, 401
    
    user_id = PermissionService.get_current_user_id()
    from models import User
    user = User.query.get(user_id)
    
    if user is None:
        return {'error': 'User not found'}, 404
    
    return user.to_dict(), 200
