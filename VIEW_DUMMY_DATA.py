import requests
import time

time.sleep(3)

BASE_URL = 'http://127.0.0.1:5000/api'

# Login
r = requests.post(f'{BASE_URL}/auth/login', 
                  json={'username': 'john_doe', 'password': 'password123'})
cookies = r.cookies

# Get lists
r2 = requests.get(f'{BASE_URL}/lists', cookies=cookies)
lists = r2.json()

print("=" * 80)
print("LIST COMPLETION STATUS")
print("=" * 80)
for lst in lists:
    status = "✅ ALL DONE!" if lst.get('all_completed') else "⏳ In Progress"
    print(f"\n{lst['title']}: {status}")
    print(f"  Tasks: {lst.get('completed_count', 0)}/{lst.get('task_count', 0)} completed")
    print(f"  All completed flag: {lst.get('all_completed', False)}")
