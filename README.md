# Hierarchical Todo List Web Application

**CS162 Assignment 2** - Full-stack hierarchical todo list with React frontend and Flask backend

A professional-grade web application for managing hierarchical todo lists with user authentication, data isolation, and strategic database indexing. Built with Flask, SQLAlchemy (3NF normalized), and React TypeScript.

## 📹 Demo Video

**[Watch the Full Demo (5 minutes)](https://www.loom.com/share/076eeca7f49a4d449bdb9fdfde6431a4)**

*Screen recording demonstrating authentication, hierarchical tasks, collapsing, moving items, and database architecture*

---

## 🎯 Key Features

✅ **Multi-user authentication** - Secure login with session-based auth  
✅ **Hierarchical tasks** - Up to 3 levels of nesting (items → sub-items → sub-sub-items)  
✅ **Collapse/expand** - Hide/show subtasks to focus on important work  
✅ **Move tasks** - Relocate top-level tasks between lists  
✅ **Mark complete** - Toggle task completion status with visual feedback  
✅ **Data isolation** - Users only see their own tasks  
✅ **3NF database** - Normalized schema with cascading deletes  
✅ **77 unit tests** - 100% pass rate with 74% code coverage  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- Conda or venv for Python virtual environment

### Installation (Windows)

```powershell
# 1. Extract the ZIP and navigate to project
cd "CS162---Web-application"

# 2. Activate conda environment or create one
conda activate sage
# OR: python -m venv venv; venv\Scripts\activate.bat

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Seed database with demo data
python seed.py

# 5. Run Flask backend (Terminal 1)
python run.py
```

Backend runs at: **http://localhost:5000**

### Frontend Setup (Terminal 2)

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at: **http://localhost:3001**

### Access the App

1. Open browser to **http://localhost:3001**
2. Login with demo account:
   - Username: `john_doe`
   - Password: `password123`
3. Explore your todo lists!

---

## 📁 Project Structure

```
CS162---Web-application/
├── app/
│   ├── routes/
│   │   ├── auth.py              # Login, register, logout endpoints
│   │   └── todo.py              # TodoList & TodoItem CRUD endpoints
│   └── services/
│       ├── auth.py              # Authentication business logic
│       ├── permission.py        # Authorization & access control
│       ├── validators.py        # Request validation
│       └── __init__.py          # Service exports
├── models/
│   ├── user.py                  # User model (3NF)
│   ├── todo_list.py             # TodoList model (3NF)
│   ├── todo_item.py             # TodoItem model (hierarchical, 3NF)
│   └── __init__.py              # SQLAlchemy initialization
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components (Button, Card, etc.)
│   │   ├── contexts/            # State management (AuthContext, TaskContext)
│   │   ├── pages/               # Pages (LoginPage, DashboardPage, ListPage)
│   │   ├── services/            # API integration (api.ts, auth.ts, tasks.ts)
│   │   ├── types/               # TypeScript interfaces
│   │   ├── App.tsx              # Main component
│   │   └── main.tsx             # React entry point
│   ├── package.json             # Node.js dependencies
│   ├── vite.config.ts           # Vite configuration
│   └── tailwind.config.js       # Tailwind CSS config
├── tests/
│   ├── conftest.py              # Shared test fixtures
│   ├── test_models.py           # 17 database model tests
│   ├── test_routes.py           # 28 API endpoint tests
│   └── test_services.py         # 32 business logic tests
├── instance/
│   └── app.db                   # SQLite database (auto-created)
├── run.py                       # Flask entry point
├── seed.py                      # Database seeder with demo data
├── config.py                    # Flask configuration (dev/prod/test)
├── requirements.txt             # Python dependencies
├── DATABASE_SCHEMA.md           # ER diagram & schema documentation
└── README.md                    # This file
```

---

## 🏗️ Architecture Overview

### Design Patterns Implemented

**Service Layer Pattern** - Business logic centralized in services for testability and reusability
```python
# Routes handle HTTP
@todo_bp.route('/items', methods=['POST'])
def create_item():
    # Services handle business logic
    item = TodoItemService.create_item(list_id, parent_id, title, priority)
    return item.to_dict(), 201
```

**Strategy Pattern** - Authentication system supports multiple strategies without code changes

**Factory Pattern** - Application factory creates different app instances for different environments

**Blueprint Pattern** - Flask blueprints organize routes by domain (auth, todo)

### Database Design (3NF Normalized)

Three normalized tables with strategic indices:

| Table | Fields | Purpose |
|-------|--------|---------|
| **USER** | id, username, email, password_hash, created_at, updated_at | User authentication |
| **TODOLIST** | id, user_id, title, description, created_at, updated_at | User's todo lists |
| **TODOITEM** | id, list_id, parent_id, title, description, priority, is_completed, is_collapsed, order, created_at, updated_at | Hierarchical items |

**Key Features:**
- ✅ **3NF Normalization** - Eliminates redundancy, ensures data integrity
- ✅ **ACID Compliance** - Atomicity, Consistency, Isolation, Durability
- ✅ **Strategic Indexing** - 10 single + 4 composite indices optimize queries
- ✅ **Cascade Deletes** - Maintain referential integrity
- ✅ **Self-Referential Hierarchy** - TodoItem.parent_id → TodoItem.id (supports 3-level max)

See **`DATABASE_SCHEMA.md`** for detailed ERD and index strategy.

---

## 🧪 Testing & Code Coverage

### Test Results

| Metric | Result |
|--------|--------|
| **Total Tests** | 77 |
| **Pass Rate** | 100% ✅ |
| **Code Coverage** | 74% (494/617 lines) |
| **Execution Time** | 16.86 seconds |

### Test Breakdown

| Layer | Tests | Coverage | Focus |
|-------|-------|----------|-------|
| Models | 17 tests | 88% | User, TodoList, TodoItem with relationships |
| Routes | 28 tests | 74% | Auth, Lists, Items endpoints with HTTP status |
| Services | 32 tests | 82% | Authentication, Permissions, Validators |

### Running Tests

```powershell
# Run all tests with verbose output
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=app --cov=models --cov-report=html

# View coverage in browser
start htmlcov/index.html

# Run specific test file
python -m pytest tests/test_models.py -v

# Run specific test
python -m pytest tests/test_routes.py::test_register_user -v
```

See **`UNIT_TESTING_REPORT.md`** for detailed test descriptions and coverage analysis.

---

## 📚 API Documentation

All endpoints require JSON headers and session-based authentication.

### Authentication Endpoints

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}

Response (201):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}

Response (200): User object + session cookie
Error (401): {"error": "Invalid credentials"}
```

#### Get Current User
```
GET /api/auth/me

Response (200): User object
Error (401): {"error": "Not authenticated"}
```

#### Logout
```
POST /api/auth/logout

Response (200): {"message": "Logged out successfully"}
```

### Todo List Endpoints

#### Get All Lists
```
GET /api/lists

Response (200): [{"id": 1, "title": "Shopping", "items": [...], ...}]
```

#### Create List
```
POST /api/lists
Content-Type: application/json

{
  "title": "Shopping List",
  "description": "Grocery items"
}

Response (201): List object
```

#### Update List
```
PUT /api/lists/<list_id>
Content-Type: application/json

{"title": "Updated Title"}

Response (200): Updated list
Error (403): User doesn't own list
```

#### Delete List
```
DELETE /api/lists/<list_id>

Response (200): Success
Error (403): User doesn't own list
```

### Todo Item Endpoints

#### Create Item
```
POST /api/items
Content-Type: application/json

{
  "list_id": 1,
  "parent_id": null,           # null for root level
  "title": "Buy milk",
  "description": "2% milk",
  "priority": "medium"          # low|medium|high|urgent
}

Response (201): Item object
Error (409): Max depth reached
```

#### Update Item
```
PUT /api/items/<item_id>
Content-Type: application/json

{
  "title": "Updated title",
  "is_completed": true,
  "priority": "high"
}

Response (200): Updated item
```

#### Move Item
```
PUT /api/items/<item_id>/move
Content-Type: application/json

{
  "list_id": 2,
  "parent_id": null
}

Response (200): Moved item
Error (409): Cannot move to self or descendant
```

#### Delete Item
```
DELETE /api/items/<item_id>

Response (200): Success
Note: Cascades to all descendants
```

See routes files for complete endpoint documentation.

---

## 🎨 Frontend Features

### Modern UI/UX
- **Gradient backgrounds** with glassmorphism effects
- **Smooth animations** using Framer Motion
- **Responsive design** for desktop and mobile
- **Toast notifications** for user feedback
- **Loading spinners** during operations
- **Beautiful empty states** with helpful prompts

### Dashboard View
- Grid layout of all your todo lists
- Click any list to view its tasks
- Create new lists with sidebar button
- Visual progress bars showing completion %

### List View (Hierarchical Tasks)
- **Tree structure** showing parent-child relationships
- **Collapse/expand** buttons to hide/show subtasks
- **Drag-and-drop** interface (implemented)
- **Color-coded priorities** (low=blue, medium=yellow, high=orange, urgent=red)
- **Depth badges** showing nesting level (Level 1, 2, 3)
- **Action buttons** for edit, delete, move tasks

### State Management
- **AuthContext** - Manages login state and current user
- **TaskContext** - Manages todo lists, items, and operations
- Custom hooks for task operations (useTaskItemLogic)

---

## 🔐 Security Features

✅ **Password Hashing** - Werkzeug generate_password_hash with salting  
✅ **Session Management** - Secure session cookies with HTTPOnly flag  
✅ **Data Isolation** - SQL queries filtered by user_id  
✅ **Permission Checking** - Every endpoint verifies user ownership  
✅ **CSRF Protection** - Session-based (Lax SameSite policy)  
✅ **Input Validation** - All request fields validated before processing  

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Database**: SQLite (PostgreSQL compatible)
- **Auth**: Session-based with werkzeug password hashing
- **Testing**: Pytest, pytest-cov
- **Python**: 3.11+

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS + PostCSS
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Node**: 18+

### DevOps
- **Configuration**: Environment-based (dev/prod/test)
- **Database Migrations**: SQLAlchemy with Flask-Migrate ready
- **Testing**: 77 unit tests with 74% coverage
- **Linting**: (Configured but optional)

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| **DATABASE_SCHEMA.md** | ERD diagram, 3NF explanation, index strategy, ACID properties |
| **UNIT_TESTING_REPORT.md** | 77 tests listed with descriptions and coverage analysis |
| **HOW_TO_RUN.md** | Detailed setup instructions for Windows and macOS |
| **README.md** | This file - project overview and quick start |

---

## 🐛 Troubleshooting

### Port Already in Use

**Backend (Flask)**:
```powershell
# Change port in run.py or use:
set FLASK_PORT=5001
python run.py
```

**Frontend (Vite)**:
```powershell
# Change port in vite.config.ts or use:
npm run dev -- --port 3002
```

### Database Issues

```powershell
# Delete corrupted database and reseed
rm instance/app.db
python seed.py
```

### Tests Failing

```powershell
# Ensure database is seeded
python seed.py

# Run specific test for debugging
python -m pytest tests/test_models.py::test_user_creation -v
```

### Module Not Found

```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 📝 Notes for Grader

- **Video Demo**: All features demonstrated in 5-minute recording (linked above)
- **Code Quality**: 77 passing tests with 74% code coverage
- **Documentation**: Database schema fully documented with ERD
- **Database**: 3NF normalized with strategic indexing (see DATABASE_SCHEMA.md)
- **Security**: User data isolation enforced at SQL and API levels
- **Architecture**: Clean separation with Service layer pattern
- **Setup**: Follow Quick Start section above - no special configuration needed

---

## 📦 Submission Contents

This ZIP file contains:
- ✅ All source code (backend + frontend)
- ✅ All dependencies (requirements.txt, package.json)
- ✅ 77 unit tests with conftest fixtures
- ✅ Database schema documentation
- ✅ API documentation
- ✅ Screen recording link (in README)
- ✅ Setup instructions
- ⚠️ **NO virtual environment** (venv is not portable)

---

## 📄 License

This project is created for CS162 Assignment 2 educational purposes.

---

**Last Updated**: November 2024  
**Status**: ✅ Complete & Tested  
**Demo**: https://www.loom.com/share/076eeca7f49a4d449bdb9fdfde6431a4
