"""
Test automatic parent completion when all children are done
"""
import requests
import time

BASE_URL = 'http://127.0.0.1:5000/api'

# Wait for server to start
time.sleep(3)

print("=" * 80)
print("TESTING AUTOMATIC PARENT COMPLETION")
print("=" * 80)

# Login first
print("\n1. Logging in...")
login_response = requests.post(
    f'{BASE_URL}/auth/login',
    json={'username': 'john_doe', 'password': 'password123'}
)
print(f"Login status: {login_response.status_code}")
cookies = login_response.cookies

# Get Work Projects list (list #2)
print("\n2. Getting Work Projects list...")
list_response = requests.get(f'{BASE_URL}/lists/2', cookies=cookies)
print(f"Status: {list_response.status_code}")

if list_response.status_code == 200:
    data = list_response.json()
    
    # Find "Project Alpha" item (has children)
    project_alpha = None
    for item in data['items']:
        if item['title'] == 'Project Alpha':
            project_alpha = item
            break
    
    if project_alpha:
        print(f"\n3. Found 'Project Alpha' (ID: {project_alpha['id']})")
        print(f"   Has {len(project_alpha.get('children', []))} children")
        print(f"   Is completed: {project_alpha['is_completed']}")
        
        # First, uncomplete Project Alpha if it's completed
        if project_alpha['is_completed']:
            print("\n4. Uncompleting Project Alpha first...")
            requests.put(
                f"{BASE_URL}/items/{project_alpha['id']}",
                json={'is_completed': False},
                cookies=cookies
            )
        
        # Complete all children one by one
        print(f"\n5. Completing all children of 'Project Alpha'...")
        children = project_alpha.get('children', [])
        
        for i, child in enumerate(children, 1):
            # If child has grandchildren, complete them first
            for grandchild in child.get('children', []):
                print(f"   Completing grandchild: {grandchild['title']}")
                requests.put(
                    f"{BASE_URL}/items/{grandchild['id']}",
                    json={'is_completed': True},
                    cookies=cookies
                )
            
            print(f"   [{i}/{len(children)}] Completing: {child['title']}")
            response = requests.put(
                f"{BASE_URL}/items/{child['id']}",
                json={'is_completed': True},
                cookies=cookies
            )
            
            # After completing last child, check parent status
            if i == len(children):
                print("\n6. All children completed! Checking parent status...")
                time.sleep(0.5)
                
                # Get the parent item to see if it auto-completed
                parent_response = requests.get(
                    f"{BASE_URL}/items/{project_alpha['id']}",
                    cookies=cookies
                )
                
                if parent_response.status_code == 200:
                    parent_data = parent_response.json()
                    if parent_data['is_completed']:
                        print(f"   ✅ SUCCESS! 'Project Alpha' auto-completed!")
                        print(f"   Parent is now marked as completed: {parent_data['is_completed']}")
                    else:
                        print(f"   ❌ Parent not auto-completed")
                        print(f"   Parent completion status: {parent_data['is_completed']}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
