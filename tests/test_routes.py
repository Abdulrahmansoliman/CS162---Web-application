"""
Integration tests for API routes.

Tests cover:
- Authentication endpoints (register, login, logout, me)
- TodoList endpoints (create, read, update, delete, complete all)
- TodoItem endpoints (create, read, update, delete, move, complete, collapse)
- Permission checks and error handling
"""

from models import db, User, TodoList, TodoItem
from werkzeug.security import generate_password_hash


class TestAuthRoutes:
    """Test suite for authentication routes."""
    
    def test_register_success(self, client, app):
        """Test successful user registration."""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['username'] == 'newuser'
        assert 'user_id' in data
    
    def test_register_duplicate_username(self, client, app):
        """Test registration with duplicate username."""
        # Create first user
        client.post('/api/auth/register', json={
            'username': 'duplicate',
            'email': 'user1@example.com',
            'password': 'password'
        })
        
        # Try to register with same username
        response = client.post('/api/auth/register', json={
            'username': 'duplicate',
            'email': 'user2@example.com',
            'password': 'password'
        })
        
        assert response.status_code == 409
        assert 'already exists' in response.get_json()['error'].lower()
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields."""
        response = client.post('/api/auth/register', json={
            'username': 'incomplete'
        })
        
        assert response.status_code == 400
    
    def test_login_success(self, client, app):
        """Test successful login."""
        # Register user
        client.post('/api/auth/register', json={
            'username': 'logintest',
            'email': 'login@test.com',
            'password': 'password123'
        })
        
        # Login
        response = client.post('/api/auth/login', json={
            'username': 'logintest',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['username'] == 'logintest'
    
    def test_login_wrong_password(self, client, app):
        """Test login with wrong password."""
        # Register user
        client.post('/api/auth/register', json={
            'username': 'wrongpass',
            'email': 'wrong@test.com',
            'password': 'correctpassword'
        })
        
        # Try login with wrong password
        response = client.post('/api/auth/login', json={
            'username': 'wrongpass',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
    
    def test_login_user_not_found(self, client):
        """Test login with non-existent user."""
        response = client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'password'
        })
        
        assert response.status_code == 401
    
    def test_logout(self, client, app):
        """Test logout endpoint."""
        # Register and login
        client.post('/api/auth/register', json={
            'username': 'logouttest',
            'email': 'logout@test.com',
            'password': 'password'
        })
        client.post('/api/auth/login', json={
            'username': 'logouttest',
            'password': 'password'
        })
        
        # Logout
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 200
        assert 'message' in response.get_json()
    
    def test_get_current_user_authenticated(self, authenticated_client):
        """Test getting current user info when authenticated."""
        client, user_id = authenticated_client
        
        response = client.get('/api/auth/me')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['username'] == 'authuser'
    
    def test_get_current_user_not_authenticated(self, client):
        """Test getting current user when not authenticated."""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401


class TestTodoListRoutes:
    """Test suite for TodoList routes."""
    
    def test_create_list_authenticated(self, authenticated_client):
        """Test creating a list when authenticated."""
        client, user_id = authenticated_client
        
        response = client.post('/api/lists', json={
            'title': 'New List',
            'description': 'Test list'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'New List'
        assert data['description'] == 'Test list'
        assert data['user_id'] == user_id
    
    def test_create_list_not_authenticated(self, client):
        """Test creating a list when not authenticated."""
        response = client.post('/api/lists', json={
            'title': 'Should Fail',
            'description': 'No auth'
        })
        
        assert response.status_code == 401
    
    def test_create_list_missing_title(self, authenticated_client):
        """Test creating a list without title."""
        client, user_id = authenticated_client
        
        response = client.post('/api/lists', json={
            'description': 'No title'
        })
        
        assert response.status_code == 400
    
    def test_get_all_lists(self, authenticated_client, app):
        """Test getting all user's lists."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create lists
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
        
        response = client.get('/api/lists')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) >= 2
    
    def test_get_list_by_id(self, authenticated_client, app):
        """Test getting a specific list with items."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create list with item
            todo_list = TodoList(
                user_id=user_id,
                title='Specific List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            item = TodoItem(
                list_id=todo_list.id,
                title='Item in list',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            list_id = todo_list.id
        
        response = client.get(f'/api/lists/{list_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Specific List'
        assert 'items' in data
        assert len(data['items']) > 0
    
    def test_get_list_not_owned(self, authenticated_client, app):
        """Test getting a list not owned by user."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create another user and their list
            other_user = User(
                username='other',
                email='other@test.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(other_user)
            db.session.commit()
            
            other_list = TodoList(
                user_id=other_user.id,
                title='Not Mine',
                description='Other user'
            )
            db.session.add(other_list)
            db.session.commit()
            list_id = other_list.id
        
        response = client.get(f'/api/lists/{list_id}')
        
        assert response.status_code == 403
    
    def test_update_list(self, authenticated_client, app):
        """Test updating a list."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='Original Title',
                description='Original'
            )
            db.session.add(todo_list)
            db.session.commit()
            list_id = todo_list.id
        
        response = client.put(f'/api/lists/{list_id}', json={
            'title': 'Updated Title',
            'description': 'Updated Description'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Title'
        assert data['description'] == 'Updated Description'
    
    def test_delete_list(self, authenticated_client, app):
        """Test deleting a list."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='To Delete',
                description='Will be deleted'
            )
            db.session.add(todo_list)
            db.session.commit()
            list_id = todo_list.id
        
        response = client.delete(f'/api/lists/{list_id}')
        
        assert response.status_code == 200
        
        # Verify deleted
        with app.app_context():
            assert TodoList.query.get(list_id) is None
    
    def test_complete_all_tasks(self, authenticated_client, app):
        """Test marking all tasks complete in a list."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create list with items
            todo_list = TodoList(
                user_id=user_id,
                title='Complete All Test',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
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
            list_id = todo_list.id
        
        response = client.patch(f'/api/lists/{list_id}/complete-all')
        
        assert response.status_code == 200
        
        # Verify all complete
        with app.app_context():
            items = TodoItem.query.filter_by(list_id=list_id).all()
            assert all(item.is_completed for item in items)


class TestTodoItemRoutes:
    """Test suite for TodoItem routes."""
    
    def test_create_item(self, authenticated_client, app):
        """Test creating a todo item."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='Test List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            list_id = todo_list.id
        
        response = client.post('/api/items', json={
            'list_id': list_id,
            'title': 'New Task',
            'description': 'Task description',
            'priority': 'high',
            'order': 0
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'New Task'
        assert data['priority'] == 'high'
    
    def test_create_nested_item(self, authenticated_client, app):
        """Test creating a nested item (subtask)."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create list and parent item
            todo_list = TodoList(
                user_id=user_id,
                title='Test List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            parent = TodoItem(
                list_id=todo_list.id,
                title='Parent Task',
                order=0
            )
            db.session.add(parent)
            db.session.commit()
            list_id = todo_list.id
            parent_id = parent.id
        
        response = client.post('/api/items', json={
            'list_id': list_id,
            'parent_id': parent_id,
            'title': 'Child Task',
            'order': 0
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['parent_id'] == parent_id
        assert data['title'] == 'Child Task'
    
    def test_get_item(self, authenticated_client, app):
        """Test getting a specific item."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='Test List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            item = TodoItem(
                list_id=todo_list.id,
                title='Test Item',
                description='Description',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
        
        response = client.get(f'/api/items/{item_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Test Item'
    
    def test_update_item(self, authenticated_client, app):
        """Test updating an item."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='Test List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            item = TodoItem(
                list_id=todo_list.id,
                title='Original',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
        
        response = client.put(f'/api/items/{item_id}', json={
            'title': 'Updated',
            'priority': 'urgent'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated'
        assert data['priority'] == 'urgent'
    
    def test_delete_item(self, authenticated_client, app):
        """Test deleting an item."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='Test List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            item = TodoItem(
                list_id=todo_list.id,
                title='To Delete',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
        
        response = client.delete(f'/api/items/{item_id}')
        
        assert response.status_code == 200
        
        # Verify deleted
        with app.app_context():
            assert TodoItem.query.get(item_id) is None
    
    def test_toggle_complete(self, authenticated_client, app):
        """Test toggling item completion status."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='Test List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            item = TodoItem(
                list_id=todo_list.id,
                title='Toggle Me',
                is_completed=False,
                order=0
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
        
        # Toggle to complete
        response = client.put(
            f'/api/items/{item_id}',
            json={'is_completed': True}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['is_completed'] is True
        
        # Toggle back to incomplete
        response = client.put(
            f'/api/items/{item_id}',
            json={'is_completed': False}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['is_completed'] is False
    
    def test_toggle_collapse(self, authenticated_client, app):
        """Test toggling item collapse status."""
        client, user_id = authenticated_client
        
        with app.app_context():
            todo_list = TodoList(
                user_id=user_id,
                title='Test List',
                description='Test'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            item = TodoItem(
                list_id=todo_list.id,
                title='Collapsible',
                is_collapsed=False,
                order=0
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
        
        response = client.put(
            f'/api/items/{item_id}',
            json={'is_collapsed': True}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['is_collapsed'] is True
    
    def test_move_item_to_different_list(self, authenticated_client, app):
        """Test moving item to a different list."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create two lists
            list1 = TodoList(user_id=user_id, title='List 1')
            list2 = TodoList(user_id=user_id, title='List 2')
            db.session.add_all([list1, list2])
            db.session.commit()
            
            # Item in list1
            item = TodoItem(
                list_id=list1.id,
                title='Movable',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            item_id = item.id
            list2_id = list2.id
        
        response = client.patch(f'/api/items/{item_id}/move', json={
            'target_list_id': list2_id
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['list_id'] == list2_id


class TestPermissionEnforcement:
    """Test that permission checks are enforced."""
    
    def test_cannot_access_other_users_list(self, authenticated_client, app):
        """Test that users cannot access other users' lists."""
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
                title='Private List',
                description='Belongs to other user'
            )
            db.session.add(other_list)
            db.session.commit()
            list_id = other_list.id
        
        # Try to get other user's list
        response = client.get(f'/api/lists/{list_id}')
        assert response.status_code == 403
        
        # Try to update other user's list
        response = client.put(f'/api/lists/{list_id}', json={
            'title': 'Hacked'
        })
        assert response.status_code == 403
        
        # Try to delete other user's list
        response = client.delete(f'/api/lists/{list_id}')
        assert response.status_code == 403
    
    def test_cannot_access_other_users_items(self, authenticated_client, app):
        """Test that users cannot access other users' items."""
        client, user_id = authenticated_client
        
        with app.app_context():
            # Create another user with list and item
            other_user = User(
                username='otheruser2',
                email='other2@test.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(other_user)
            db.session.commit()
            
            other_list = TodoList(
                user_id=other_user.id,
                title='Other List'
            )
            db.session.add(other_list)
            db.session.commit()
            
            other_item = TodoItem(
                list_id=other_list.id,
                title='Private Item',
                order=0
            )
            db.session.add(other_item)
            db.session.commit()
            item_id = other_item.id
        
        # Try to get other user's item
        response = client.get(f'/api/items/{item_id}')
        assert response.status_code == 403
        
        # Try to update other user's item
        response = client.put(f'/api/items/{item_id}', json={
            'title': 'Hacked'
        })
        assert response.status_code == 403
        
        # Try to delete other user's item
        response = client.delete(f'/api/items/{item_id}')
        assert response.status_code == 403
