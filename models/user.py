"""
User Model - 3NF Normalized
Stores user authentication and account information
ACID Properties:
  - Atomicity: Single user record transaction
  - Consistency: Unique constraints on username/email
  - Isolation: Session-level isolation
  - Durability: Persisted in database
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):
    """
    User account model with authentication support.
    
    NORMALIZATION: 3NF
    - No repeating groups (atomic values only)
    - All non-key attributes depend on primary key
    - No transitive dependencies
    
    INDEXING STRATEGY:
    - username: UNIQUE INDEX (login queries)
    - email: UNIQUE INDEX (password reset, lookups)
    - created_at: INDEX (user list sorting)
    """
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Core Attributes (Atomic values - 1NF)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Metadata (Functional dependency on id - 2NF, 3NF)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (Foreign key relationships)
    todo_lists = db.relationship(
        'TodoList',
        backref='owner',
        lazy='select',  # Explicit load for performance
        cascade='all, delete-orphan',  # ACID: cascading deletes
        foreign_keys='TodoList.user_id'
    )
    
    def set_password(self, password):
        """Hash and set user password (ACID: atomic operation)"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
