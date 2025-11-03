# How to Run the Application

This guide follows the **exact installation steps** required by the CS162 Assignment 2 specifications.

---

## 📋 Assignment Required Installation Step├── instance/                 # SQLite database location
├── app.py                   # Backend entry point ⭐ (REQUIRED)
├── seed.py                  # Database seeder
### **Flask on Windows:**

```powershell
python3 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3 app.py
```

### **Node.js (Frontend):**

```powershell
cd frontend
npm install
npm start
```

---

## 🚀 Complete Setup Instructions

### **Step 1: Extract the ZIP file**

Extract the assignment ZIP file to your desired location.

---

### **Step 2: Navigate to Project Directory**

```powershell
cd "path\to\CS162---Web-application"
```

Example:
```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application"
```

---

### **Step 3: Set Up Python Virtual Environment**

Create a virtual environment:

```powershell
python3 -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate.bat
```

**Expected output:**
```
(venv) C:\Users\...\CS162---Web-application>
```

You should see `(venv)` at the start of your prompt.

---

### **Step 4: Install Python Dependencies**

```powershell
pip3 install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 ...
```

---

### **Step 5: Seed the Database** (One-time setup)

```powershell
python3 seed.py
```

**What this does:**
- Creates SQLite database in `instance/app.db`
- Adds 3 demo users with sample todo lists
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

### **Step 6: Start the Backend Server**

```powershell
python3 app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
```

✅ **Backend is now running on http://127.0.0.1:5000**

❌ **Keep this terminal running!** Don't close it.

---

### **Step 7: Start the Frontend** (New Terminal)

Open a **NEW PowerShell terminal** and run:

```powershell
cd "path\to\CS162---Web-application\frontend"
npm install
npm start
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

✅ **Frontend is now running on http://localhost:5173** (or http://localhost:5174 if 5173 is taken)

❌ **Keep this terminal running too!**

---

## 🌐 Access the Application

Once both servers are running, open your browser and go to:

```
http://localhost:5173
```

(Or check the terminal output for the actual port number)

---

## 👤 Demo Login Credentials

Use these credentials to test the application:

| Username | Password | Description |
|----------|----------|-------------|
| `john_doe` | `password123` | User with shopping & work lists |
| `jane_smith` | `password456` | User with study & fitness lists |
| `bob_wilson` | `password789` | User with home & travel lists |

---

## 📂 Project Structure

```
CS162---Web-application/
├── app/                     # Flask application
│   ├── __init__.py         # Application factory
│   ├── routes/             # API endpoints (auth, todo)
│   └── services/           # Business logic (auth, permissions)
├── models/                  # Database models (User, TodoList, TodoItem)
├── tests/                   # Unit tests (77 tests, 74% coverage)
├── frontend/                # React + TypeScript application
│   ├── src/                # React components and pages
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── instance/                # SQLite database location
├── app.py                   # Backend entry point ⭐ (REQUIRED)
├── seed.py                  # Database seeder script
├── requirements.txt         # Python dependencies
├── config.py               # Flask configuration
└── README.md               # Project documentation
```

---

## 🎯 What You Should See

### **Terminal 1 (Backend):**
```
(venv) PS C:\...\CS162---Web-application> python3 app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### **Terminal 2 (Frontend):**
```
PS C:\...\CS162---Web-application\frontend> npm start

> hierarchical-todo-frontend@1.0.0 start
> vite

  VITE v5.0.8  ready in 450 ms

  ➜  Local:   http://localhost:5173/
```

### **Browser:**
- Login page with beautiful gradient background
- Enter username: `john_doe`, password: `password123`
- See hierarchical todo lists with collapse/expand functionality

---

## 🛠️ Troubleshooting

### **Problem: `python3: command not found`**

**Solution:** Try `python` instead of `python3`:
```powershell
python -m venv venv
python app.py
```

### **Problem: `venv\Scripts\activate.bat` not working**

**Solution:** Use PowerShell activation:
```powershell
venv\Scripts\Activate.ps1
```

If you get an error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problem: Port 5000 already in use**

**Solution:** Kill the process or change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001)
```

### **Problem: Frontend port 5173 already in use**

**Solution:** Vite will automatically try the next available port (5174, 5175, etc.)
Check the terminal output for the actual port.

### **Problem: `npm install` fails**

**Solution:** Clear npm cache and try again:
```powershell
npm cache clean --force
npm install
```

### **Problem: Backend crashes on Windows**

**Solution:** The app automatically disables auto-reload on Windows.
If you still have issues, set:
```powershell
$env:FLASK_USE_RELOADER="0"
python3 app.py
```

---

## ✅ Features to Test

Once the app is running, test these features:

- ✅ **Multi-user support** - Login with different users
- ✅ **Data isolation** - Each user sees only their own tasks
- ✅ **Create lists** - Add new todo lists
- ✅ **Hierarchical tasks** - Add subtasks up to 3 levels deep
- ✅ **Mark complete** - Toggle task completion status
- ✅ **Collapse/expand** - Hide/show subtasks
- ✅ **Move tasks** - Relocate tasks between lists
- ✅ **Drag-and-drop** - Reorder tasks visually
- ✅ **Priority levels** - Set task priorities (low, medium, high, urgent)
- ✅ **Responsive design** - Works on different screen sizes

---

## 📝 Running Tests

To run the 77 unit tests:

```powershell
# Make sure virtual environment is activated
venv\Scripts\activate.bat

# Run tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov=models --cov-report=html
```

**Expected output:**
```
======================== 77 passed in 2.34s =========================
```

---

## 🎬 Demo Video

Watch the full demo video here:
**https://www.loom.com/share/076eeca7f49a4d449bdb9fdfde6431a4**

---

## 📧 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify both terminals are running
3. Check browser console for errors (F12)
4. Verify database was seeded successfully

---

**Enjoy using the Hierarchical Todo List Application! 🎉**

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
PS C:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application> python3 app.py
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
├── app/                     # Flask application
├── models/                  # Database models
├── tests/                   # Unit tests (77 tests)
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
