import requests
import time

BASE_URL = 'http://127.0.0.1:5000/api'

# Give server time to start if needed
time.sleep(1)

try:
    print("Testing GET /lists endpoint...")
    response = requests.get(f'{BASE_URL}/lists', timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        lists = response.json()
        print(f"✅ Got {len(lists)} lists")
        if lists:
            list_id = lists[0]['id']
            print(f"\nTesting GET /lists/{list_id} endpoint...")
            response = requests.get(f'{BASE_URL}/lists/{list_id}', timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS! Got list with {len(data.get('items', []))} items")
                # Show first item
                if data.get('items'):
                    item = data['items'][0]
                    print(f"\nFirst item: {item['title']}")
                    if 'children' in item:
                        print(f"Has {len(item['children'])} children")
            else:
                print(f"❌ Failed: {response.text[:200]}")
    else:
        print(f"❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")
