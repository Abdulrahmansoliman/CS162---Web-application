"""
Pytest configuration and fixtures for testing.

This module provides shared fixtures for all tests including:
- Flask app instance
- Database setup/teardown
- Test client
- Authenticated user sessions
"""

import pytest
from app import create_app
from models import db, User, TodoList, TodoItem
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='function')
def app():
    """
    Create and configure a test Flask application instance.
    
    Uses in-memory SQLite database for fast, isolated tests.
    Each test function gets a fresh database.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """
    Create a test client for making HTTP requests.
    
    Returns:
        FlaskClient: Test client for API testing
    """
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """
    Create a test CLI runner.
    
    Returns:
        FlaskCliRunner: CLI runner for testing commands
    """
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def init_database(app):
    """
    Initialize database with test data.
    
    Creates sample users, lists, and items for testing.
    """
    with app.app_context():
        # Create test users
        user1 = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123')
        )
        user2 = User(
            username='otheruser',
            email='other@example.com',
            password_hash=generate_password_hash('password456')
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # Create test lists
        list1 = TodoList(
            user_id=user1.id,
            title='Test List 1',
            description='First test list'
        )
        list2 = TodoList(
            user_id=user1.id,
            title='Test List 2',
            description='Second test list'
        )
        list3 = TodoList(
            user_id=user2.id,
            title='Other User List',
            description='Belongs to other user'
        )
        db.session.add_all([list1, list2, list3])
        db.session.commit()
        
        # Create test items with hierarchy
        item1 = TodoItem(
            list_id=list1.id,
            title='Parent Task',
            description='Top level task',
            order=0
        )
        db.session.add(item1)
        db.session.commit()
        
        item2 = TodoItem(
            list_id=list1.id,
            parent_id=item1.id,
            title='Child Task',
            description='Nested task',
            order=0
        )
        db.session.add(item2)
        db.session.commit()
        
        yield db


@pytest.fixture(scope='function')
def authenticated_client(client, app):
    """
    Create an authenticated test client.
    
    Returns:
        tuple: (client, user_id) - Client with active session and user ID
    """
    with app.app_context():
        # Create user
        user = User(
            username='authuser',
            email='auth@example.com',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    # Login
    response = client.post('/api/auth/login', json={
        'username': 'authuser',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    
    return client, user_id


@pytest.fixture(scope='function')
def sample_user(app):
    """
    Create a sample user in the database.
    
    Returns:
        User: User model instance
    """
    with app.app_context():
        user = User(
            username='sampleuser',
            email='sample@example.com',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture(scope='function')
def sample_list(app, sample_user):
    """
    Create a sample todo list.
    
    Returns:
        TodoList: TodoList model instance
    """
    with app.app_context():
        user = User.query.filter_by(username='sampleuser').first()
        todo_list = TodoList(
            user_id=user.id,
            title='Sample List',
            description='Sample description'
        )
        db.session.add(todo_list)
        db.session.commit()
        return todo_list


@pytest.fixture(scope='function')
def sample_item(app, sample_list):
    """
    Create a sample todo item.
    
    Returns:
        TodoItem: TodoItem model instance
    """
    with app.app_context():
        todo_list = TodoList.query.filter_by(title='Sample List').first()
        item = TodoItem(
            list_id=todo_list.id,
            title='Sample Item',
            description='Sample task',
            order=0
        )
        db.session.add(item)
        db.session.commit()
        return item
