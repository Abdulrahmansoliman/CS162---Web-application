# Quick Start Guide

Get the application running with dummy data in 3 steps.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Seed the Database

Populate with dummy data (3 users, 6 lists, 26 items):

```bash
python seed.py
```

You'll see:
```
🗑️  Clearing existing data...
👤 Creating users...
✅ Created 3 users: john_doe, jane_smith, bob_wilson
...
✅ DATABASE SEEDING COMPLETE!

🔐 Test Credentials:
   1. john_doe / password123
   2. jane_smith / password456
   3. bob_wilson / password789
```

## Step 3: Run the Application

```bash
python run.py
```

Server starts on `http://localhost:5000`

## Test the Backend

### Via cURL (Windows PowerShell):

```powershell
# Register a new user
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/auth/register" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Login
$loginBody = @{
    username = "john_doe"
    password = "password123"
} | ConvertTo-Json

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $loginBody `
    -WebSession $session

# Get user lists (using session with cookies)
Invoke-WebRequest -Uri "http://localhost:5000/api/lists" `
    -Method GET `
    -WebSession $session

# Get first list with items
Invoke-WebRequest -Uri "http://localhost:5000/api/lists/1" `
    -Method GET `
    -WebSession $session
```

### Via Python:

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"
session = requests.Session()

# Login
response = session.post(f"{BASE_URL}/auth/login", json={
    "username": "john_doe",
    "password": "password123"
})
print("Login:", response.json())

# Get user's lists
lists = session.get(f"{BASE_URL}/lists")
print("Lists:", lists.json())

# Get first list with items
list_detail = session.get(f"{BASE_URL}/lists/1")
print("List with items:", json.dumps(list_detail.json(), indent=2))

# Get specific item with children (hierarchical)
item = session.get(f"{BASE_URL}/items/1")
print("Item with children:", json.dumps(item.json(), indent=2))

# Create new item
new_item = session.post(f"{BASE_URL}/items", json={
    "list_id": 1,
    "parent_id": None,
    "title": "New Item",
    "description": "Test item"
})
print("Created:", new_item.json())

# Update item
updated = session.put(f"{BASE_URL}/items/1", json={
    "is_completed": True,
    "title": "Updated Title"
})
print("Updated:", updated.json())

# Logout
session.post(f"{BASE_URL}/auth/logout")
print("Logged out")
```

## Test Data Structure

### User: john_doe

**Lists:**
1. Shopping List (10 items, 3 levels deep)
   - Produce
     - Apples (with details)
     - Bananas
     - Carrots
   - Dairy
     - Milk
     - Cheese
     - Yogurt
   - Meat & Protein
   - Snacks

2. Work Projects (5 items)
   - Project Alpha
     - Design
       - Wireframes
       - Prototype
     - Development
   - Project Beta

3. Home Maintenance (3 items)
   - Clean kitchen
   - Fix leaky faucet
   - Mow lawn

### User: jane_smith

**Lists:**
1. Personal Goals
   - Learn Python
   - Read 12 books
   - Plan Europe trip

2. Fitness Plan
   - Gym workouts
   - Running routine

### User: bob_wilson

**Lists:**
1. Development Tasks
   - Fix critical bugs
   - Code review
   - Write documentation

## Available Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user

### TodoLists
- `POST /api/lists` - Create list
- `GET /api/lists` - Get all lists
- `GET /api/lists/{id}` - Get list with items
- `PUT /api/lists/{id}` - Update list
- `DELETE /api/lists/{id}` - Delete list

### TodoItems
- `POST /api/items` - Create item
- `GET /api/items/{id}` - Get item with children
- `PUT /api/items/{id}` - Update item
- `DELETE /api/items/{id}` - Delete item
- `PATCH /api/items/{id}/move` - Move item

## Troubleshooting

### "Flask not found"
```bash
pip install -r requirements.txt
```

### "Database locked"
Delete `dev.db` and run `seed.py` again

### Port 5000 in use
Change port in `run.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Use 5001 instead
```

### CORS Issues (for frontend)
Add to `app/__init__.py`:
```python
from flask_cors import CORS
CORS(app)
```

Then install: `pip install flask-cors`

## Next Steps

1. ✅ Backend running with dummy data
2. 📦 Create React frontend to display/manage todos
3. 🎨 Add UI components for hierarchical tasks
4. 🔍 Test full CRUD operations
5. 🚀 Deploy to production

See README.md for full API documentation.
