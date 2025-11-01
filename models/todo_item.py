"""
TodoItem Model - 3NF Normalized with Hierarchical Support
Supports recursive task hierarchy with optimized indices
ACID Properties:
  - Atomicity: Single item transaction
  - Consistency: Referential integrity with cascades
  - Isolation: User-based isolation (via list_id)
  - Durability: Persisted in database
"""

from datetime import datetime
from . import db


class TodoItem(db.Model):
    """
    Hierarchical todo item model with self-referential relationship.
    Supports recursive structure for subtasks.
    
    NORMALIZATION: 3NF
    - Atomic values only (1NF)
    - Non-key attributes depend on primary key (2NF)
    - No transitive dependencies (3NF)
    - No repeating groups in hierarchy
    
    INDEXING STRATEGY FOR RECURSIVE QUERIES:
    - list_id: INDEX (fetch items for a list)
    - parent_id: INDEX (fetch children of item - CRITICAL for recursion)
    - user_id (via list): IMPLICIT (via foreign key)
    - is_collapsed: INDEX (filter visible items)
    - is_completed: INDEX (filter active tasks)
    - order: INDEX (sort items)
    - Composite: (list_id, parent_id): INDEX (most common query)
    - Composite: (parent_id, order): INDEX (fetch children sorted)
    
    RECURSIVE QUERY OPTIMIZATION:
    When fetching tree structure, indices enable:
    1. Quick parent lookup (parent_id)
    2. Quick children lookup (list_id + parent_id)
    3. Efficient ordering (order field + index)
    """
    __tablename__ = 'todo_items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys (Referential integrity - ACID)
    list_id = db.Column(
        db.Integer,
        db.ForeignKey('todo_lists.id', ondelete='CASCADE'),
        nullable=False,
        index=True  # INDEX: Quick fetch for list items
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('todo_items.id', ondelete='CASCADE'),
        nullable=True,
        index=True  # INDEX: CRITICAL for recursive queries
    )
    
    # Core Attributes (Atomic - 1NF)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # State Attributes (Functional dependencies on id - 2NF, 3NF)
    is_completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True  # INDEX: Filter for active/done tasks
    )
    is_collapsed = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        index=True  # INDEX: Filter for UI rendering
    )
    
    # Ordering (For consistent display - denormalized for performance)
    order = db.Column(
        db.Integer,
        default=0,
        nullable=False,
        index=True  # INDEX: Sort items without additional sorts
    )
    
    # Metadata (Temporal attributes - 2NF, 3NF)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True  # INDEX: Sort by creation time
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Self-referential relationship for hierarchy
    children = db.relationship(
        'TodoItem',
        remote_side=[id],
        backref=db.backref('parent', remote_side=[parent_id]),
        lazy='select',  # Explicit loading for control
        cascade='all, delete-orphan',  # ACID: cascade deletes
        foreign_keys=[parent_id],
        single_parent=True  # Allow delete-orphan on self-referential relationship
    )
    
    # Composite indices for optimal query performance
    __table_args__ = (
        # Composite index for fetching items in a list with parent
        db.Index('idx_list_parent', 'list_id', 'parent_id'),
        # Composite index for children with ordering
        db.Index('idx_parent_order', 'parent_id', 'order'),
        # Composite for filtering collapsed/completed with ordering
        db.Index('idx_parent_collapsed_order', 'parent_id',
                 'is_collapsed', 'order'),
        # Composite for fetching active tasks
        db.Index('idx_parent_completed', 'parent_id', 'is_completed'),
    )
    
    def get_depth(self):
        """
        Calculate depth in hierarchy.
        Used to enforce max 3 levels constraint.
        Traverses upward to root.
        
        Performance: O(depth) - max 3 for MVP
        """
        depth = 0
        current = self.parent
        while current is not None:
            depth += 1
            current = current.parent
        return depth
    
    def can_add_child(self):
        """
        Check if this item can have children.
        MVP constraint: max 3 levels (depth must be < 2)
        """
        return self.get_depth() < 2
    
    def get_all_descendants(self):
        """
        Recursively get all descendants.
        Used for cascade operations and cleanup.
        
        Performance: O(n) where n = total descendants
        Indices optimize child fetching at each level
        """
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def to_dict(self, include_children=False):
        """Convert to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'list_id': self.list_id,
            'parent_id': self.parent_id,
            'title': self.title,
            'description': self.description,
            'is_completed': self.is_completed,
            'is_collapsed': self.is_collapsed,
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'depth': self.get_depth()
        }
        if include_children:
            data['children'] = [
                child.to_dict(include_children=True)
                for child in self.children
            ]
        return data
    
    def __repr__(self):
        return f'<TodoItem {self.title} (depth={self.get_depth()})>'
