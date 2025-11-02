# How to Run the Application

This guide shows you exactly how to run the CS162 Todo Application on your Windows machine.

---

## 📋 Prerequisites

Before running the application, make sure you have:
- ✅ Python 3.12+ installed
- ✅ Node.js & npm installed
- ✅ Virtual environment (`.venv`) set up
- ✅ Dependencies installed from `requirements.txt` and `package.json`

---

## 🚀 Quick Start (3 Steps)

### **Step 1: Seed the Database** (One-time setup)

Open PowerShell and run:

```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application"
.\.venv\bin\python.exe seed.py
```

**What this does:**
- Creates SQLite database in `instance/app.db`
- Adds 3 demo users: `john_doe`, `jane_smith`, `bob_wilson`
- Creates sample todo lists and tasks
- Ready for testing!

**Expected output:**
```
🗑️  Clearing existing data...
👤 Creating users...
✅ Created 3 users: john_doe, jane_smith, bob_wilson
📋 Creating todo lists...
✅ All data seeded successfully!
```

---

### **Step 2: Start the Backend Server**

Open **PowerShell Terminal 1** and run:

```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application"
.\.venv\bin\python.exe run.py
```

**What this does:**
- Starts Flask backend server
- Listens on `http://127.0.0.1:5000`
- Enables debug mode with auto-reload

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

❌ **Keep this terminal running!** Don't close it while using the app.

---

### **Step 3: Start the Frontend**

Open **PowerShell Terminal 2** and run:

```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application\frontend"
npm run dev
```

**What this does:**
- Starts Vite development server
- Bundles React + TypeScript
- Runs on `http://localhost:5173` (or `3000/3001` if port taken)

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

## 🌐 Access the Application

Once both servers are running, open your browser:

```
http://localhost:5173
```

Or if port 5173 is taken, check the terminal output for the correct port.

---

## 🔑 Demo Login Credentials

Use these credentials to test the application:

```
Username: john_doe
Password: password123
```

Or:
```
Username: jane_smith
Password: password456
```

Or:
```
Username: bob_wilson
Password: password789
```

---

## 📋 Complete Terminal Setup

Here's what your screen should look like:

### **Terminal 1 - Backend**
```powershell
PS C:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application> .\.venv\bin\python.exe run.py
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### **Terminal 2 - Frontend**
```powershell
PS C:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application\frontend> npm run dev
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

## 🧪 Running Unit Tests

In a **new PowerShell terminal**, run:

```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application"
.\.venv\bin\python.exe -m pytest tests/ -v
```

**With coverage report:**
```powershell
.\.venv\bin\python.exe -m pytest tests/ -v --cov=app --cov=models --cov-report=html
start htmlcov/index.html
```

**Expected output:**
```
77 passed in 16.86s
```

---

## ⚠️ Troubleshooting

### **Port Already in Use**

**Backend (5000)**:
```powershell
# Kill the process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Frontend (5173)**:
```powershell
# Kill the process using port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### **Python Module Not Found**

Make sure virtual environment is activated and dependencies are installed:
```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

### **npm Dependencies Missing**

```powershell
cd frontend
npm install
npm run dev
```

### **Database Issues**

Reseed the database:
```powershell
.\.venv\bin\python.exe seed.py
```

---

## 📁 Project Structure

```
CS162---Web-application/
├── backend/
│   ├── app/                 # Flask application
│   ├── models/              # Database models
│   ├── tests/               # Unit tests (77 tests)
│   ├── run.py               # Backend entry point
│   └── seed.py              # Database seeder
│
├── frontend/                # React application
│   ├── src/                 # Source code
│   ├── package.json         # Dependencies
│   └── npm run dev          # Frontend entry point
│
└── documentation/
    ├── README.md            # Project overview
    ├── HOW_TO_RUN.md        # This file
    ├── UNIT_TESTING_REPORT.md
    └── DATABASE_SCHEMA.md
```

---

## 🎯 Features to Test

Once logged in, you can:

✅ **Create Todo Lists** - Click "New List" in sidebar  
✅ **Add Tasks** - Click "Add Task" in list view  
✅ **Hierarchical Tasks** - Add subtasks (up to 3 levels deep)  
✅ **Complete Tasks** - Click checkbox to mark done  
✅ **Collapse/Expand** - Hide subtasks with arrow icon  
✅ **Move Tasks** - Drag or use "Move to List" button  
✅ **Delete** - Remove lists/tasks with confirmation  
✅ **Logout** - Click your username in top right  

---

## 📊 Application Details

- **Backend**: Flask 3.0.0 + SQLAlchemy
- **Frontend**: React 18.2.0 + TypeScript
- **Database**: SQLite (instance/app.db)
- **Authentication**: Session-based with werkzeug
- **Tests**: 77 unit tests (100% pass rate)
- **Coverage**: 74% code coverage

---

## 📞 Support

For detailed information, see:
- `README.md` - Project overview
- `UNIT_TESTING_REPORT.md` - Testing details
- `DATABASE_SCHEMA.md` - Database structure

---

**Happy coding! 🚀**
