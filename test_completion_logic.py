"""
Test hierarchical completion logic
"""
import requests
import time

BASE_URL = 'http://127.0.0.1:5000/api'

# Wait for server to start
time.sleep(3)

print("=" * 80)
print("TESTING HIERARCHICAL COMPLETION LOGIC")
print("=" * 80)

# Login first
print("\n1. Logging in...")
login_response = requests.post(
    f'{BASE_URL}/auth/login',
    json={'username': 'john_doe', 'password': 'password123'}
)
print(f"Login status: {login_response.status_code}")
cookies = login_response.cookies

# Get list 1 (Shopping List)
print("\n2. Getting Shopping List...")
list_response = requests.get(f'{BASE_URL}/lists/1', cookies=cookies)
print(f"Status: {list_response.status_code}")

if list_response.status_code == 200:
    data = list_response.json()
    
    # Find "Produce" item (has children)
    produce_item = None
    for item in data['items']:
        if item['title'] == 'Produce':
            produce_item = item
            break
    
    if produce_item:
        print(f"\n3. Found 'Produce' item (ID: {produce_item['id']})")
        print(f"   Has {len(produce_item.get('children', []))} children")
        print(f"   Is completed: {produce_item['is_completed']}")
        
        # Try to complete parent without completing children
        print("\n4. Trying to complete 'Produce' (should fail - children not completed)...")
        update_response = requests.put(
            f"{BASE_URL}/items/{produce_item['id']}",
            json={'is_completed': True},
            cookies=cookies
        )
        print(f"   Status: {update_response.status_code}")
        if update_response.status_code == 400:
            print(f"   ✅ Correctly rejected: {update_response.json().get('error')}")
        else:
            print(f"   ❌ Should have been rejected!")
        
        # Complete all children first
        print("\n5. Completing all children of 'Produce'...")
        for child in produce_item.get('children', []):
            # If child has grandchildren, complete them first
            for grandchild in child.get('children', []):
                print(f"   Completing grandchild: {grandchild['title']}")
                requests.put(
                    f"{BASE_URL}/items/{grandchild['id']}",
                    json={'is_completed': True},
                    cookies=cookies
                )
            
            print(f"   Completing child: {child['title']}")
            child_response = requests.put(
                f"{BASE_URL}/items/{child['id']}",
                json={'is_completed': True},
                cookies=cookies
            )
            print(f"   Status: {child_response.status_code}")
        
        # Now try to complete parent
        print("\n6. Now completing 'Produce' (should succeed)...")
        update_response = requests.put(
            f"{BASE_URL}/items/{produce_item['id']}",
            json={'is_completed': True},
            cookies=cookies
        )
        print(f"   Status: {update_response.status_code}")
        if update_response.status_code == 200:
            print(f"   ✅ Successfully completed!")
            result = update_response.json()
            print(f"   Is completed: {result['is_completed']}")
        
        # Test adding new child to completed parent
        print("\n7. Adding new child to completed 'Produce' (should uncomplete parent)...")
        new_child_response = requests.post(
            f"{BASE_URL}/items",
            json={
                'list_id': 1,
                'parent_id': produce_item['id'],
                'title': 'Test New Item'
            },
            cookies=cookies
        )
        print(f"   Status: {new_child_response.status_code}")
        
        # Check if parent is now uncompleted
        print("\n8. Checking if 'Produce' is now uncompleted...")
        item_response = requests.get(f"{BASE_URL}/items/{produce_item['id']}", cookies=cookies)
        if item_response.status_code == 200:
            result = item_response.json()
            if not result['is_completed']:
                print(f"   ✅ Parent correctly uncompleted!")
            else:
                print(f"   ❌ Parent should be uncompleted!")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
