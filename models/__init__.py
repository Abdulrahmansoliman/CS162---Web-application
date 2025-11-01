"""
Modular database models package
Implements 3NF normalization, ACID properties, and optimized indexing
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Import all models to make them available
from .user import User
from .todo_list import TodoList
from .todo_item import TodoItem

__all__ = ['db', 'User', 'TodoList', 'TodoItem']
