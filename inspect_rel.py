import sys
sys.path.insert(0, '.')

from app import create_app, db
from models import TodoItem
from sqlalchemy import inspect

app = create_app('development')
with app.app_context():
    # Use inspect to look at the relationship
    mapper = inspect(TodoItem)
    print("TodoItem Relationships:")
    for rel_name, rel in mapper.relationships.items():
        print(f"\n{rel_name}:")
        print(f"  Type: {type(rel)}")
        print(f"  Direction: {rel.direction}")
        print(f"  uselist: {rel.uselist}")
        print(f"  mapper: {rel.mapper.class_.__name__}")
        print(f"  local side: {rel.local_columns}")
        print(f"  remote side: {rel.remote_side}")
    
    # Now check an actual item
    item = TodoItem.query.filter_by(id=1).first()
    print(f"\n\nItem 1 ({item.title}):")
    print(f"  parent_id: {item.parent_id}")
    print(f"  children attribute: {item.children}")
    print(f"  children type: {type(item.children)}")
    
    # Check a child item
    item5 = TodoItem.query.filter_by(id=5).first()
    print(f"\nItem 5 ({item5.title}):")
    print(f"  parent_id: {item5.parent_id}")
    print(f"  parent: {item5.parent}")
    print(f"  children: {item5.children}")
