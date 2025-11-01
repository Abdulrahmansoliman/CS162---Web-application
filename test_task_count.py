import requests
import time

time.sleep(3)

BASE_URL = 'http://127.0.0.1:5000/api'

# Login
r = requests.post(f'{BASE_URL}/auth/login', json={'username': 'john_doe', 'password': 'password123'})
cookies = r.cookies

# Get lists
r2 = requests.get(f'{BASE_URL}/lists', cookies=cookies)
lists = r2.json()

print("Lists with task counts:")
for l in lists:
    print(f"  - {l['title']}: {l.get('task_count', 'N/A')} tasks")
