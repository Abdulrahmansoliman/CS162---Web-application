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
    """

    __tablename__ = 'todo_items'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys (Referential integrity)
    list_id = db.Column(
        db.Integer,
        db.ForeignKey('todo_lists.id', ondelete='CASCADE'),
        nullable=False,
        index=True  # fetch items by list quickly
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('todo_items.id', ondelete='CASCADE'),
        nullable=True,
        index=True  # critical for recursive queries
    )

    # Core attributes
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # State
    is_completed = db.Column(db.Boolean, default=False, nullable=False, index=True)
    is_collapsed = db.Column(db.Boolean, default=False, nullable=False, index=True)

    # Ordering (map to existing DB column 'order')
    order = db.Column(
        'order',
        db.Integer,
        default=0,
        nullable=False,
        index=True
    )

    # Timestamps
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

    # Self-referential relationship for hierarchy
    # NOTE: remote_side must be on the many-to-one side (the backref 'parent')
    children = db.relationship(
        'TodoItem',
        backref=db.backref('parent', uselist=False, remote_side=[id]),
        lazy='selectin',                 # efficient eager loading for trees
        cascade='all, delete-orphan',    # delete-orphan requires single_parent
        foreign_keys=[parent_id],
        single_parent=True
    )

    # Composite indices for common patterns
    __table_args__ = (
        db.Index('idx_list_parent', 'list_id', 'parent_id'),
        db.Index('idx_parent_order', 'parent_id', 'order'),
        db.Index('idx_parent_collapsed_order', 'parent_id', 'is_collapsed', 'order'),
        db.Index('idx_parent_completed', 'parent_id', 'is_completed'),
    )

    # --------- Helpers ---------

    def get_depth(self) -> int:
        """
        Calculate depth in hierarchy by walking up to root.
        Performance: O(depth).
        """
        depth = 0
        current = self.parent
        while current is not None:
            depth += 1
            current = current.parent
        return depth

    def can_add_child(self) -> bool:
        """
        MVP constraint: allow max 3 levels total -> depth < 2 can add a child.
        """
        return self.get_depth() < 2

    def get_all_descendants(self):
        """
        Recursively collect all descendants.
        Performance: O(n) where n is number of descendants.
        """
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants

    def all_children_completed(self) -> bool:
        """
        Check if all direct children are completed.
        Uses BFS-like approach (checking immediate children only).
        Returns True if no children or all children are completed.
        """
        if not self.children:
            return True
        return all(child.is_completed for child in self.children)

    def can_be_completed(self) -> bool:
        """
        A task can only be marked as completed if all its children are completed.
        This enforces bottom-up completion (leaf tasks first).
        """
        return self.all_children_completed()

    def uncomplete_parent_chain(self):
        """
        When a new subtask is added or a child becomes uncompleted,
        propagate uncompleted status up the parent chain.
        """
        current = self.parent
        while current is not None:
            if current.is_completed:
                current.is_completed = False
            current = current.parent

    def to_dict(self, include_children: bool = False):
        """Serialize to dict for JSON responses."""
        data = {
            'id': self.id,
            'list_id': self.list_id,
            'parent_id': self.parent_id,
            'title': self.title,
            'description': self.description,
            'is_completed': self.is_completed,
            'is_collapsed': self.is_collapsed,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'depth': self.get_depth(),
        }
        if include_children:
            data['children'] = [child.to_dict(include_children=True) for child in self.children]
        return data

    def __repr__(self):
        return f'<TodoItem {self.title} (depth={self.get_depth()})>'
