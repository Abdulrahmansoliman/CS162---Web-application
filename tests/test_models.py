"""
Unit tests for database models.

Tests cover:
- User model (creation, validation, password hashing)
- TodoList model (creation, relationships, validation)
- TodoItem model (hierarchy, completion logic, relationships)
"""

import pytest
from models import db, User, TodoList, TodoItem
from werkzeug.security import check_password_hash, generate_password_hash


class TestUserModel:
    """Test suite for User model."""
    
    def test_create_user(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User(
                username='newuser',
                email='new@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'newuser'
            assert user.email == 'new@example.com'
            assert user.created_at is not None
    
    def test_password_hashing(self, app):
        """Test that passwords are properly hashed."""
        with app.app_context():
            password = 'securepassword123'
            user = User(
                username='testuser',
                email='test@example.com',
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            
            # Password should be hashed
            assert user.password_hash != password
            # But should verify correctly
            assert check_password_hash(user.password_hash, password)
            # Wrong password should fail
            assert not check_password_hash(user.password_hash, 'wrongpassword')
    
    def test_unique_username(self, app):
        """Test that usernames must be unique."""
        with app.app_context():
            user1 = User(
                username='duplicate',
                email='user1@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(user1)
            db.session.commit()
            
            # Try to create another user with same username
            user2 = User(
                username='duplicate',
                email='user2@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(user2)
            
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()
    
    def test_unique_email(self, app):
        """Test that emails must be unique."""
        with app.app_context():
            user1 = User(
                username='user1',
                email='same@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(user1)
            db.session.commit()
            
            # Try to create another user with same email
            user2 = User(
                username='user2',
                email='same@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(user2)
            
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()
    
    def test_user_to_dict(self, app):
        """Test User.to_dict() method."""
        with app.app_context():
            user = User(
                username='dictuser',
                email='dict@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            
            assert user_dict['username'] == 'dictuser'
            assert user_dict['email'] == 'dict@example.com'
            assert 'password_hash' not in user_dict  # Should not expose password
            assert 'id' in user_dict
            assert 'created_at' in user_dict


class TestTodoListModel:
    """Test suite for TodoList model."""
    
    def test_create_list(self, app, sample_user):
        """Test creating a new todo list."""
        with app.app_context():
            user = User.query.filter_by(username='sampleuser').first()
            todo_list = TodoList(
                user_id=user.id,
                title='New List',
                description='Test description'
            )
            db.session.add(todo_list)
            db.session.commit()
            
            assert todo_list.id is not None
            assert todo_list.title == 'New List'
            assert todo_list.description == 'Test description'
            assert todo_list.user_id == user.id
            assert todo_list.created_at is not None
    
    def test_list_items_relationship(self, app, sample_list):
        """Test TodoList-TodoItem relationship."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            # Add items to list
            item1 = TodoItem(
                list_id=todo_list.id,
                title='Item 1',
                order=0
            )
            item2 = TodoItem(
                list_id=todo_list.id,
                title='Item 2',
                order=1
            )
            db.session.add_all([item1, item2])
            db.session.commit()
            
            # Test relationship
            assert len(todo_list.items) >= 2
            titles = [item.title for item in todo_list.items]
            assert 'Item 1' in titles
            assert 'Item 2' in titles
    
    def test_list_to_dict(self, app, sample_list):
        """Test TodoList.to_dict() method."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            list_dict = todo_list.to_dict()
            
            assert list_dict['title'] == 'Sample List'
            assert list_dict['description'] == 'Sample description'
            assert 'id' in list_dict
            assert 'user_id' in list_dict
            assert 'created_at' in list_dict
    
    def test_cascade_delete_list(self, app, sample_list):
        """Test that deleting a list deletes its items (cascade)."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            list_id = todo_list.id
            
            # Add items
            item = TodoItem(
                list_id=list_id,
                title='Will be deleted',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            
            # Delete list
            db.session.delete(todo_list)
            db.session.commit()
            
            # Items should be deleted too
            items = TodoItem.query.filter_by(list_id=list_id).all()
            assert len(items) == 0


class TestTodoItemModel:
    """Test suite for TodoItem model."""
    
    def test_create_item(self, app, sample_list):
        """Test creating a new todo item."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            item = TodoItem(
                list_id=todo_list.id,
                title='New Task',
                description='Task description',
                priority='high',
                order=0
            )
            db.session.add(item)
            db.session.commit()
            
            assert item.id is not None
            assert item.title == 'New Task'
            assert item.description == 'Task description'
            assert item.priority == 'high'
            assert item.is_completed is False
            assert item.is_collapsed is False
            assert item.parent_id is None
    
    def test_item_hierarchy(self, app, sample_list):
        """Test parent-child hierarchy."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            # Create parent
            parent = TodoItem(
                list_id=todo_list.id,
                title='Parent Task',
                order=0
            )
            db.session.add(parent)
            db.session.commit()
            
            # Create children
            child1 = TodoItem(
                list_id=todo_list.id,
                parent_id=parent.id,
                title='Child 1',
                order=0
            )
            child2 = TodoItem(
                list_id=todo_list.id,
                parent_id=parent.id,
                title='Child 2',
                order=1
            )
            db.session.add_all([child1, child2])
            db.session.commit()
            
            # Test relationships
            assert len(parent.children) == 2
            assert child1.parent.title == 'Parent Task'
            assert child2.parent.title == 'Parent Task'
    
    def test_can_be_completed(self, app, sample_list):
        """Test can_be_completed() logic."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            # Parent with no children can be completed
            parent = TodoItem(
                list_id=todo_list.id,
                title='Parent',
                order=0
            )
            db.session.add(parent)
            db.session.commit()
            
            assert parent.can_be_completed() is True
            
            # Add incomplete child - parent cannot be completed
            child = TodoItem(
                list_id=todo_list.id,
                parent_id=parent.id,
                title='Child',
                is_completed=False,
                order=0
            )
            db.session.add(child)
            db.session.commit()
            
            assert parent.can_be_completed() is False
            
            # Complete child - parent can now be completed
            child.is_completed = True
            db.session.commit()
            
            assert parent.can_be_completed() is True
    
    def test_auto_complete_parent_chain(self, app, sample_list):
        """Test auto-completion of parent chain."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            # Create 3-level hierarchy
            grandparent = TodoItem(
                list_id=todo_list.id,
                title='Grandparent',
                order=0
            )
            db.session.add(grandparent)
            db.session.commit()
            
            parent = TodoItem(
                list_id=todo_list.id,
                parent_id=grandparent.id,
                title='Parent',
                order=0
            )
            db.session.add(parent)
            db.session.commit()
            
            child = TodoItem(
                list_id=todo_list.id,
                parent_id=parent.id,
                title='Child',
                order=0
            )
            db.session.add(child)
            db.session.commit()
            
            # Complete child (only child)
            child.is_completed = True
            child.auto_complete_parent_chain()
            db.session.commit()
            
            # Refresh from DB
            db.session.refresh(parent)
            db.session.refresh(grandparent)
            
            # Parent and grandparent should auto-complete
            assert parent.is_completed is True
            assert grandparent.is_completed is True
    
    def test_uncomplete_parent_chain(self, app, sample_list):
        """Test uncompleting parent chain."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            # Create hierarchy with completed items
            parent = TodoItem(
                list_id=todo_list.id,
                title='Parent',
                is_completed=True,
                order=0
            )
            db.session.add(parent)
            db.session.commit()
            
            child = TodoItem(
                list_id=todo_list.id,
                parent_id=parent.id,
                title='Child',
                is_completed=True,
                order=0
            )
            db.session.add(child)
            db.session.commit()
            
            # Uncomplete child
            child.is_completed = False
            child.uncomplete_parent_chain()
            db.session.commit()
            
            # Refresh from DB
            db.session.refresh(parent)
            
            # Parent should be uncompleted
            assert parent.is_completed is False
    
    def test_item_to_dict(self, app, sample_item):
        """Test TodoItem.to_dict() method."""
        with app.app_context():
            item = TodoItem.query.filter_by(title='Sample Item').first()
            item_dict = item.to_dict()
            
            assert item_dict['title'] == 'Sample Item'
            assert item_dict['description'] == 'Sample task'
            assert 'id' in item_dict
            assert 'list_id' in item_dict
            assert 'is_completed' in item_dict
            assert 'is_collapsed' in item_dict
            assert 'priority' in item_dict
    
    def test_cascade_delete_item(self, app, sample_list):
        """Test that deleting a parent deletes children (cascade)."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            # Create parent and child
            parent = TodoItem(
                list_id=todo_list.id,
                title='Parent to Delete',
                order=0
            )
            db.session.add(parent)
            db.session.commit()
            
            child = TodoItem(
                list_id=todo_list.id,
                parent_id=parent.id,
                title='Child to Delete',
                order=0
            )
            db.session.add(child)
            db.session.commit()
            
            parent_id = parent.id
            child_id = child.id
            
            # Delete parent
            db.session.delete(parent)
            db.session.commit()
            
            # Child should be deleted
            assert TodoItem.query.get(child_id) is None
    
    def test_priority_values(self, app, sample_list):
        """Test priority field accepts valid values."""
        with app.app_context():
            todo_list = TodoList.query.filter_by(title='Sample List').first()
            
            priorities = ['low', 'medium', 'high', 'urgent']
            
            for priority in priorities:
                item = TodoItem(
                    list_id=todo_list.id,
                    title=f'{priority.capitalize()} Priority Task',
                    priority=priority,
                    order=0
                )
                db.session.add(item)
                db.session.commit()
                
                assert item.priority == priority
