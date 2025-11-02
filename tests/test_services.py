"""
Unit tests for service layer.

Tests cover:
- AuthenticationService and strategies
- PermissionService
- RequestValidator
- ErrorResponse and SuccessResponse
- TodoListService and TodoItemService
"""

import pytest
from flask import session
from models import db, User, TodoList, TodoItem
from app.services.auth import AuthenticationService, LocalAuthStrategy
from app.services.permission import PermissionService
from app.services.validators import RequestValidator, ErrorResponse, SuccessResponse
from app.services.todo_service import TodoListService, TodoItemService
from werkzeug.security import generate_password_hash


class TestAuthenticationService:
    """Test suite for AuthenticationService."""
    
    def test_local_auth_strategy_success(self, app):
        """Test successful authentication with LocalAuthStrategy."""
        with app.app_context():
            # Create user
            user = User(
                username='authtest',
                email='auth@test.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            # Test authentication
            strategy = LocalAuthStrategy()
            result = strategy.authenticate(
                username='authtest',
                password='password123'
            )
            
            assert result is not None
            assert result.username == 'authtest'
            assert result.email == 'auth@test.com'
    
    def test_local_auth_strategy_wrong_password(self, app):
        """Test authentication failure with wrong password."""
        with app.app_context():
            user = User(
                username='authtest',
                email='auth@test.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            strategy = LocalAuthStrategy()
            result = strategy.authenticate(
                username='authtest',
                password='wrongpassword'
            )
            
            assert result is None
    
    def test_local_auth_strategy_user_not_found(self, app):
        """Test authentication failure with non-existent user."""
        with app.app_context():
            strategy = LocalAuthStrategy()
            result = strategy.authenticate(
                username='nonexistent',
                password='password123'
            )
            
            assert result is None
    
    def test_auth_service_with_strategy(self, app):
        """Test AuthenticationService with strategy pattern."""
        with app.app_context():
            user = User(
                username='strategytest',
                email='strategy@test.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            # Create service with strategy
            auth_service = AuthenticationService(LocalAuthStrategy())
            result = auth_service.authenticate(
                username='strategytest',
                password='password123'
            )
            
            assert result is not None
            assert result.username == 'strategytest'


class TestPermissionService:
    """Test suite for PermissionService."""
    
    def test_get_current_user_id_authenticated(self, app, authenticated_client):
        """Test getting current user ID when authenticated."""
        client, user_id = authenticated_client
        
        with app.app_context():
            with client.session_transaction() as sess:
                sess['user_id'] = user_id
            
            with client:
                client.get('/')  # Make a request to establish context
                current_user_id = PermissionService.get_current_user_id()
                assert current_user_id == user_id
    
    def test_is_authenticated_true(self, app, authenticated_client):
        """Test is_authenticated returns True for logged-in user."""
        client, user_id = authenticated_client
        
        with app.app_context():
            with client.session_transaction() as sess:
                sess['user_id'] = user_id
            
            with client:
                client.get('/')
                assert PermissionService.is_authenticated() is True
    
    def test_is_authenticated_false(self, app, client):
        """Test is_authenticated returns False for guest."""
        with app.app_context():
            with client:
                client.get('/')
                assert PermissionService.is_authenticated() is False
    
    def test_owns_list_true(self, app, authenticated_client):
        """Test owns_list returns True for owned list."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create list for user
            todo_list = TodoList(
                user_id=user_id,
                title='My List',
                description='Owned by me'
            )
            db.session.add(todo_list)
            db.session.commit()
            list_id = todo_list.id
            
            with client.session_transaction() as sess:
                sess['user_id'] = user_id
            
            with client:
                client.get('/')
                assert PermissionService.owns_list(list_id) is True
    
    def test_owns_list_false(self, app, authenticated_client):
        """Test owns_list returns False for other user's list."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create another user and their list
            other_user = User(
                username='otheruser',
                email='other@test.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(other_user)
            db.session.commit()
            
            other_list = TodoList(
                user_id=other_user.id,
                title='Not My List',
                description='Owned by other'
            )
            db.session.add(other_list)
            db.session.commit()
            list_id = other_list.id
            
            with client.session_transaction() as sess:
                sess['user_id'] = user_id
            
            with client:
                client.get('/')
                assert PermissionService.owns_list(list_id) is False
    
    def test_owns_item_true(self, app, authenticated_client):
        """Test owns_item returns True for owned item."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create list and item
            todo_list = TodoList(
                user_id=user_id,
                title='My List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            item = TodoItem(
                list_id=todo_list.id,
                title='My Item',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
            
            with client.session_transaction() as sess:
                sess['user_id'] = user_id
            
            with client:
                client.get('/')
                assert PermissionService.owns_item(item_id) is True
    
    def test_get_user_lists(self, app, authenticated_client):
        """Test get_user_lists returns only user's lists."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create lists for user
            list1 = TodoList(
                user_id=user_id,
                title='List 1',
                description='First'
            )
            list2 = TodoList(
                user_id=user_id,
                title='List 2',
                description='Second'
            )
            db.session.add_all([list1, list2])
            db.session.commit()
            
            # Create list for other user
            other_user = User(
                username='other',
                email='other@test.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(other_user)
            db.session.commit()
            
            other_list = TodoList(
                user_id=other_user.id,
                title='Other List',
                description='Not mine'
            )
            db.session.add(other_list)
            db.session.commit()
            
            with client.session_transaction() as sess:
                sess['user_id'] = user_id
            
            with client:
                client.get('/')
                user_lists = PermissionService.get_user_lists()
                
                assert len(user_lists) == 2
                titles = [lst.title for lst in user_lists]
                assert 'List 1' in titles
                assert 'List 2' in titles
                assert 'Other List' not in titles


class TestRequestValidator:
    """Test suite for RequestValidator."""
    
    def test_validate_json_valid(self, app, client):
        """Test validating valid JSON request."""
        with app.test_request_context(
            json={'username': 'test', 'password': 'pass'}
        ):
            from flask import request
            data, error = RequestValidator.validate_json(request)
            assert error is None
            assert data == {'username': 'test', 'password': 'pass'}
    
    def test_validate_required_fields_all_present(self, app):
        """Test validation when all required fields present."""
        data = {'username': 'test', 'email': 'test@example.com'}
        error = RequestValidator.validate_required_fields(
            data,
            'username',
            'email'
        )
        assert error is None
    
    def test_validate_required_fields_missing(self, app):
        """Test validation when required field is missing."""
        data = {'username': 'test'}
        error = RequestValidator.validate_required_fields(
            data,
            'username',
            'email'
        )
        assert error is not None
        assert 'email' in error.lower()
    
    def test_validate_optional_field_valid(self, app):
        """Test optional field validation with valid value."""
        data = {'priority': 'high'}
        value, error = RequestValidator.validate_optional_field(
            data,
            'priority',
            ['low', 'medium', 'high', 'urgent']
        )
        assert error is None
        assert value == 'high'
    
    def test_validate_optional_field_invalid(self, app):
        """Test optional field validation with invalid value."""
        data = {'priority': 'invalid'}
        value, error = RequestValidator.validate_optional_field(
            data,
            'priority',
            ['low', 'medium', 'high', 'urgent']
        )
        assert error is not None
        assert 'priority' in error.lower()


class TestResponseHelpers:
    """Test suite for ErrorResponse and SuccessResponse."""
    
    def test_error_unauthorized(self):
        """Test ErrorResponse.unauthorized()."""
        response_dict, status_code = ErrorResponse.unauthorized(
            'Access denied'
        )
        assert status_code == 403
        assert response_dict['error'] == 'Access denied'
    
    def test_error_not_authenticated(self):
        """Test ErrorResponse.not_authenticated()."""
        response_dict, status_code = ErrorResponse.not_authenticated()
        assert status_code == 401
        assert 'not authenticated' in response_dict['error'].lower()
    
    def test_error_not_found(self):
        """Test ErrorResponse.not_found()."""
        response_dict, status_code = ErrorResponse.not_found('Resource')
        assert status_code == 404
        assert 'resource' in response_dict['error'].lower()
    
    def test_error_bad_request(self):
        """Test ErrorResponse.bad_request()."""
        response_dict, status_code = ErrorResponse.bad_request(
            'Invalid input'
        )
        assert status_code == 400
        assert response_dict['error'] == 'Invalid input'
    
    def test_success_created(self):
        """Test SuccessResponse.created()."""
        data = {'id': 1, 'title': 'Test'}
        response_dict, status_code = SuccessResponse.created(data)
        assert status_code == 201
        assert response_dict == data
    
    def test_success_ok(self):
        """Test SuccessResponse.ok()."""
        data = {'message': 'Success'}
        response_dict, status_code = SuccessResponse.ok(data)
        assert status_code == 200
        assert response_dict == data
    
    def test_success_message(self):
        """Test SuccessResponse.message()."""
        response_dict, status_code = SuccessResponse.message(
            'Operation completed'
        )
        assert status_code == 200
        assert response_dict['message'] == 'Operation completed'


class TestTodoListService:
    """Test suite for TodoListService."""
    
    def test_create_list(self, app, sample_user):
        """Test creating a list via service."""
        with app.app_context():
            user = User.query.filter_by(username='sampleuser').first()
            
            result = TodoListService.create_list(
                user_id=user.id,
                title='Service List',
                description='Created via service'
            )
            
            assert result.title == 'Service List'
            assert result.description == 'Created via service'
            assert result.user_id == user.id
    
    def test_update_list(self, app, sample_list):
        """Test updating a list via service."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            updated = TodoListService.update_list(
                todo_list,
                {
                    'title': 'Updated Title',
                    'description': 'Updated Description'
                }
            )
            
            assert updated.title == 'Updated Title'
            assert updated.description == 'Updated Description'
    
    def test_delete_list(self, app, sample_list):
        """Test deleting a list via service."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            list_id = todo_list.id
            
            TodoListService.delete_list(todo_list)
            
            # List should be deleted
            assert TodoList.query.get(list_id) is None
    
    def test_complete_all_tasks(self, app, sample_list):
        """Test marking all tasks in a list complete."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            # Add items
            item1 = TodoItem(
                list_id=todo_list.id,
                title='Task 1',
                order=0
            )
            item2 = TodoItem(
                list_id=todo_list.id,
                title='Task 2',
                order=1
            )
            db.session.add_all([item1, item2])
            db.session.commit()
            
            # Mark all complete
            TodoListService.complete_all_tasks(todo_list.id)
            
            # All items should be complete
            items = TodoItem.query.filter_by(list_id=todo_list.id).all()
            assert all(item.is_completed for item in items)


class TestTodoItemService:
    """Test suite for TodoItemService."""
    
    def test_validate_parent_success(self, app, sample_list):
        """Test parent validation succeeds for valid parent."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            parent = TodoItem(
                list_id=todo_list.id,
                title='Parent',
                order=0
            )
            db.session.add(parent)
            db.session.commit()
            
            error = TodoItemService.validate_parent(parent.id, todo_list.id)
            assert error is None
    
    def test_validate_parent_not_found(self, app, sample_list):
        """Test parent validation fails for non-existent parent."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            error = TodoItemService.validate_parent(99999, todo_list.id)
            assert error is not None
            assert 'not found' in error.lower()
    
    def test_validate_parent_wrong_list(self, app, sample_user):
        """Test parent validation fails for parent in different list."""
        with app.app_context():
            user = User.query.filter_by(username='sampleuser').first()
            
            # Create two lists
            list1 = TodoList(user_id=user.id, title='List 1')
            list2 = TodoList(user_id=user.id, title='List 2')
            db.session.add_all([list1, list2])
            db.session.commit()
            
            # Parent in list1
            parent = TodoItem(list_id=list1.id, title='Parent', order=0)
            db.session.add(parent)
            db.session.commit()
            
            # Try to use as parent in list2
            error = TodoItemService.validate_parent(parent.id, list2.id)
            assert error is not None
            assert 'same list' in error.lower()
    
    def test_create_item(self, app, sample_list):
        """Test creating an item via service."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            item = TodoItemService.create_item(
                list_id=todo_list.id,
                title='Service Item',
                description='Created via service',
                priority='high',
                order=0
            )
            
            assert item.title == 'Service Item'
            assert item.description == 'Created via service'
            assert item.priority == 'high'
            assert item.list_id == todo_list.id
    
    def test_delete_item(self, app, sample_item):
        """Test deleting an item via service."""
        with app.app_context():
            item = TodoItem.query.filter_by(title='Sample Item').first()
            item_id = item.id
            
            TodoItemService.delete_item(item)
            
            assert TodoItem.query.get(item_id) is None
