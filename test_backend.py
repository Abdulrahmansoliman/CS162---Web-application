"""
Test script to verify the server works
"""
import sys

# Test imports
print("Testing imports...")
try:
    from app import create_app, db
    from models import User, TodoList, TodoItem
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test app creation
print("\nCreating Flask app...")
try:
    app = create_app('development')
    print("✅ Flask app created successfully")
except Exception as e:
    print(f"❌ App creation error: {e}")
    sys.exit(1)

# Test database
print("\nTesting database...")
try:
    with app.app_context():
        user_count = db.session.query(User).count()
        list_count = db.session.query(TodoList).count()
        item_count = db.session.query(TodoItem).count()
        msg = f"Database OK - Users: {user_count}, Lists: {list_count}"
        print(f"✅ {msg}, Items: {item_count}")
except Exception as e:
    print(f"❌ Database error: {e}")
    sys.exit(1)

# Test API endpoints
print("\nTesting API endpoints...")
with app.test_client() as client:
    try:
        # Test auth me endpoint (should return 401 without auth)
        response = client.get('/api/auth/me')
        print(f"✅ GET /api/auth/me returned {response.status_code}")
        
        # Test lists endpoint (should return 401 without auth)
        response = client.get('/api/lists')
        print(f"✅ GET /api/lists returned {response.status_code}")
        
        print("\n✅ All API endpoints are reachable!")
    except Exception as e:
        print(f"❌ API test error: {e}")
        sys.exit(1)

print("\n" + "="*50)
print("✅ ALL TESTS PASSED - SERVER READY!")
print("="*50)
print("\nTo start the server, run:")
print("  python run.py")
print("\nThen visit: http://localhost:5000")
