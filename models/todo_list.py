"""
TodoList Model - 3NF Normalized
Represents a user's todo list
ACID Properties:
  - Atomicity: Single list record transaction
  - Consistency: Foreign key constraint to user
  - Isolation: User-based isolation
  - Durability: Persisted in database
"""

from datetime import datetime
from . import db


class TodoList(db.Model):
    """
    Todo list model owned by a user.
    
    NORMALIZATION: 3NF
    - Atomic values only (1NF)
    - Non-key attributes depend on primary key (2NF)
    - No transitive dependencies (3NF)
    - Denormalization: title/description stored here (not separate)
    
    INDEXING STRATEGY:
    - user_id: INDEX (fetch user's lists - FOREIGN KEY)
    - created_at: INDEX (sort lists by creation)
    - user_id + created_at: COMPOSITE INDEX (common query)
    """
    __tablename__ = 'todo_lists'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key (Referential integrity - ACID)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Core Attributes (Atomic - 1NF)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Metadata (Functional dependency on id - 2NF, 3NF)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships (Top-level items only, parent_id IS NULL)
    items = db.relationship(
        'TodoItem',
        backref='list',
        lazy='select',  # Explicit load for control
        cascade='all, delete-orphan',  # ACID: cascading deletes
        foreign_keys='TodoItem.list_id',
        primaryjoin='and_(TodoList.id==foreign(TodoItem.list_id), '
                   'TodoItem.parent_id==None)'
    )
    
    def to_dict(self, include_items=False):
        """Convert to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_items:
            data['items'] = [
                item.to_dict(include_children=True)
                for item in self.items
                if item.parent_id is None
            ]
        return data
    
    def __repr__(self):
        return f'<TodoList {self.title}>'
