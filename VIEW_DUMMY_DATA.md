# 🎯 Quick Guide: View Your Dummy Data

## Step 1: Make Sure Server is Running

Run this command in PowerShell:
```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application"
C:\Users\20112\anaconda3\envs\sage\python.exe run.py
```

You should see:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

## Step 2: Open the Test Page

Open your browser and go to:
**http://127.0.0.1:5000/**

This will show you a nice test interface!

## Step 3: Login with Dummy User

Click the **Login** button (it's pre-filled with `john_doe` / `password123`)

**john_doe** has:
- Shopping List (with hierarchical items)
- Work Projects
- Home Maintenance

## Step 4: View the Data

1. Click **"Get All My Lists"** - Shows all 3 lists
2. Enter list ID (1, 2, or 3) and click **"Get List with Items"** - Shows the hierarchical structure!

---

## 📋 All Available Dummy Users

Created by `seed.py`:

| Username | Password | Lists |
|----------|----------|-------|
| john_doe | password123 | 3 lists with hierarchical items |
| jane_smith | password456 | 2 lists |
| bob_wilson | password789 | 1 list |

---

## 🔍 Direct API Endpoints (for advanced users)

If you want to use tools like Postman or curl:

### 1. Login First
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","password":"password123"}' \
  -c cookies.txt
```

### 2. Get All Lists
```bash
curl http://127.0.0.1:5000/api/lists \
  -b cookies.txt
```

### 3. Get List with Items (e.g., list ID 1)
```bash
curl http://127.0.0.1:5000/api/lists/1 \
  -b cookies.txt
```

---

## 🗂️ What's in the Dummy Data?

### Shopping List (john_doe, List ID 1)
```
Shopping List
├── Produce
│   ├── Buy 2kg Apples ✅ (completed)
│   │   └── Check if organic available
│   ├── Buy Bananas
│   └── Buy Carrots
├── Dairy
│   └── Buy Milk
├── Meat & Protein ✅ (completed)
└── Snacks
```

### Work Projects (john_doe, List ID 2)
```
Work Projects
├── Complete Presentation
│   ├── Create slides
│   │   └── Add diagrams
│   └── Practice delivery
└── Code Review
```

### Home Maintenance (john_doe, List ID 3)
```
Home Maintenance
└── Fix Kitchen Sink
    └── Buy replacement parts
```

---

## 💡 Tips

- The test page at http://127.0.0.1:5000/ handles sessions automatically
- You must login first before viewing lists (all endpoints require authentication)
- The hierarchical structure shows parent-child relationships (max 3 levels)
- Items can be marked as completed (✅)
