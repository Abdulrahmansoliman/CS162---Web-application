import sys
sys.path.insert(0, '.')

from app import create_app, db
from models import TodoList, TodoItem

app = create_app('development')
with app.app_context():
    print("=" * 80)
    print("INSPECTING DATABASE")
    print("=" * 80)
    
    list1 = TodoList.query.get(1)
    print(f"\nList: {list1.title}")
    print(f"Items in list: {len(list1.items)}")
    
    if list1.items:
        item = list1.items[0]
        print(f"\nFirst item: {item.title}")
        print(f"Item ID: {item.id}")
        print(f"Item parent_id: {item.parent_id}")
        print(f"Item.children type: {type(item.children)}")
        print(f"Item.children value: {item.children}")
        print(f"Item.children is None: {item.children is None}")
        
        # Try to_dict
        print("\n--- Attempting to_dict() ---")
        try:
            result = item.to_dict(include_children=True)
            print(f"SUCCESS! to_dict result keys: {result.keys()}")
        except Exception as e:
            print(f"ERROR in to_dict: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("CHECKING ALL ITEMS IN LIST 1")
    print("=" * 80)
    
    # Check all items
    all_items = TodoItem.query.filter_by(list_id=1).all()
    print(f"Total items in list 1: {len(all_items)}")
    
    for idx, item in enumerate(all_items[:5], 1):  # First 5 items
        print(f"\nItem {idx}: {item.title}")
        print(f"  ID: {item.id}, parent_id: {item.parent_id}")
        print(f"  children type: {type(item.children)}")
        print(f"  children length: {len(item.children) if item.children else 'None'}")
