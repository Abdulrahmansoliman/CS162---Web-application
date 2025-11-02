# Hierarchical Todo List Web Application# Hierarchical Todo List Web Application



**CS162 Assignment 2** - Full-stack hierarchical todo list with React frontend and Flask backendA professional-grade web application for managing hierarchical todo lists with user authentication and data isolation. Built with Flask backend and SQLAlchemy ORM using 3NF database normalization.

## Repo Link
**[Repo link](https://github.com/Abdulrahmansoliman/CS162---Web-application/tree/main)** 

## 📹 Demo Video

**[Watch the Full Demo (5 minutes)](https://www.loom.com/share/076eeca7f49a4d449bdb9fdfde6431a4)**

*Screen recording demonstrating all features including authentication, hierarchical tasks, collapsing, moving items, and database structure*

## Architecture Overview

### Design Patterns

- **Strategy Pattern**: Authentication system supports multiple authentication strategies (local, OAuth, LDAP, etc.) without code changes

- **Factory Pattern**: Application factory allows creation of different app instances for different environments

---- **Service Layer**: Centralized business logic in services (auth, permissions) for easy testing and reusability

- **Blueprint Pattern**: Flask blueprints organize routes by domain (auth, todo)

## 🎯 Project Summary

### Database Design

A modern web application for managing hierarchical todo lists where users can:

- Create multiple todo lists- **3NF Normalization**: Ensures data integrity and eliminates redundancy

- Add nested tasks up to 3 levels deep- **ACID Compliance**: All transactions maintain Atomicity, Consistency, Isolation, Durability

- Mark tasks as complete/incomplete- **Strategic Indexing**: 10 single + 4 composite indices optimize query performance

- Collapse/expand task hierarchies- **Cascading Deletes**: Maintain referential integrity when deleting users, lists, or items

- Move tasks between lists- **Hierarchical Support**: Self-referential TodoItem with max 3-level depth constraint

- Securely manage their own data

### Key Technologies

**Live Demo**: Login at http://localhost:3001 with `john_doe` / `password123`

- **Backend**: Flask 3.0.0 + Flask-SQLAlchemy 3.1.1

---- **Database**: SQLite (easily migrates to PostgreSQL)

- **Authentication**: Session-based with werkzeug password hashing

## ✅ MVP Requirements Checklist- **Configuration**: Environment-based (Development, Production, Testing)



- [x] **Multi-user support** - Each user has isolated task workspace## Project Structure

- [x] **Authentication & Authorization** - Users only see their own tasks

- [x] **Mark tasks complete** - Toggle complete status with visual feedback```

- [x] **Collapse/expand tasks** - Hide/show subtasks to focus on important items├── app/

- [x] **Move tasks** - Relocate top-level tasks between lists│   ├── __init__.py           # Application factory

- [x] **Durable storage** - SQLite database with 3NF normalization│   ├── routes/

- [x] **3-level hierarchy limit** - Items → Sub-items → Sub-sub-items│   │   ├── auth.py          # Authentication endpoints

- [ ] **Screen recording demo** - ADD YOUR LINK ABOVE ⬆️│   │   └── todo.py          # TodoList & TodoItem endpoints

│   └── services/

---│       ├── auth.py          # Authentication service (Strategy pattern)

│       ├── permission.py    # Authorization & access control

## 🚀 Quick Start│       └── __init__.py      # Service exports

├── models/

### Installation (Flask on Windows)│   ├── __init__.py          # SQLAlchemy initialization

│   ├── user.py              # User model

```powershell│   ├── todo_list.py         # TodoList model

# 1. Extract the ZIP file│   └── todo_item.py         # TodoItem model (hierarchical)

├── config.py                 # Configuration for environments

# 2. Navigate to project directory├── run.py                    # Application entry point

cd "CS162---Web-application"├── requirements.txt          # Python dependencies

├── DATABASE_SCHEMA.md        # ER diagram and schema docs

# 3. Activate your conda environment  └── README.md                 # This file

conda activate sage```

# (Or create one: conda create -n sage python=3.12)

## Setup Instructions

# 4. Install Python dependencies

pip install -r requirements.txt### 1. Install Dependencies



# 5. Seed database with demo data```bash

python seed.pypip install -r requirements.txt

```

# 6. Run Flask backend

python run.py### 2. Run Application

```

**Development Mode** (with auto-reload and debug):

Backend runs at: **http://127.0.0.1:5000**```bash

python run.py

### Frontend Setup (React)```



Open a **new terminal window**:**Production Mode**:

```bash

```powershellset FLASK_ENV=production

# 1. Navigate to frontend folderpython run.py

cd "CS162---Web-application/frontend"```



# 2. Install dependenciesThe server runs on `http://localhost:5000`

---

## 🧪 Unit Testing & Code Coverage

### Overview

The application includes a **comprehensive test suite** with 77 tests achieving **100% pass rate** and **74% code coverage**.

**Test Results Summary:**
- ✅ **77 tests** - All passing
- ✅ **100% pass rate** - Zero failures
- ✅ **74% coverage** - 494/617 lines tested
- ⚡ **16.86 seconds** - Full suite execution time

### Test Breakdown

| Layer | Tests | Coverage | Status |
|-------|-------|----------|--------|
| **Models** (User, TodoList, TodoItem) | 17 | 88% | ✅ |
| **Routes** (Auth, Lists, Items) | 28 | 74% | ✅ |
| **Services** (Auth, Permissions, Validators) | 32 | 82% | ✅ |
| **TOTAL** | **77** | **74%** | ✅ **100%** |

### What's Tested

#### 1. Database Models (17 tests)
- User registration, password hashing, unique constraints
- TodoList CRUD operations, cascade delete, relationships
- TodoItem hierarchy (up to 3 levels), parent-child relationships, auto-completion

#### 2. API Routes (28 tests)
- Authentication: registration, login, logout, get current user
- Lists: create, read, update, delete with proper HTTP status codes
- Items: create, read, update, delete, move between lists, mark complete

#### 3. Business Logic (32 tests)
- Authentication service with Strategy pattern implementation
- Permission service enforcing user data isolation (403 Forbidden)
- Request validators for required/optional fields
- Response helpers for proper JSON serialization
- Todo services for CRUD and hierarchical operations

### Running Tests

**1. Seed the database** (create demo users):
```powershell
cd "c:\Users\20112\Downloads\cs162 assignment 2\CS162---Web-application"
.\.venv\bin\python.exe seed.py
```

**2. Run all tests:**
```powershell
.\.venv\bin\python.exe -m pytest tests/ -v
```

**3. Run with coverage report:**
```powershell
.\.venv\bin\python.exe -m pytest tests/ -v --cov=app --cov=models --cov-report=html
```

**4. View coverage report in browser:**
```powershell
start htmlcov/index.html
```

### Coverage Details by Module

| Module | Lines | Coverage | Status |
|--------|-------|----------|--------|
| `models/user.py` | 20 | **95%** | ✅ Excellent |
| `models/todo_list.py` | 23 | **96%** | ✅ Excellent |
| `app/services/validators.py` | 49 | **91%** | ✅ Excellent |
| `app/services/auth.py` | 44 | 85% | ✅ Good |
| `app/routes/auth.py` | 50 | 83% | ✅ Good |
| `models/todo_item.py` | 65 | 74% | ✅ Good |
| `app/services/permission.py` | 39 | 71% | ✅ Good |
| `app/services/todo_service.py` | 131 | 65% | ✅ Functional |
| `app/routes/todo.py` | 158 | 65% | ✅ Functional |

### Test Structure
```
tests/
├── conftest.py              # Shared fixtures (app, client, users)
├── test_models.py           # 17 database model tests
├── test_routes.py           # 28 API endpoint tests
└── test_services.py         # 32 business logic tests
```

### Key Testing Achievements

✅ **Authentication** - Registration, login, logout, sessions verified  
✅ **Data Persistence** - CRUD operations all tested  
✅ **Permissions** - User data isolation enforced  
✅ **Hierarchy** - Parent-child task relationships validated  
✅ **HTTP Status** - Correct responses (200, 201, 400, 401, 403, 404, 409)  
✅ **Validation** - Required fields, optional fields, constraints checked  
✅ **Edge Cases** - Cascade deletes, depth limits, duplicates prevented  

### For More Details

See **`UNIT_TESTING_REPORT.md`** for detailed information about:
- All 77 tests listed with descriptions
- Coverage analysis for each module
- How to run specific tests
- Interpretation of coverage reports

---

npm install

### 3. Database

# 3. Run development server

npm run devThe application automatically creates the SQLite database on first run. Database file is created at the project root as `dev.db`.

```

## API Documentation

Frontend runs at: **http://localhost:3001**

All endpoints return JSON responses. Authentication uses session-based cookies.

### Access the App

### Authentication Endpoints (`/api/auth`)

1. Open browser to **http://localhost:3001**

2. Login with demo account:#### Register User

   - Username: `john_doe````

   - Password: `password123`POST /api/auth/register

3. Explore your todo lists!Content-Type: application/json



---{

    "username": "john_doe",

## 📁 Project Structure    "email": "john@example.com",

    "password": "secure_password"

```}

CS162---Web-application/

├── app/                      # Flask backend applicationResponse (201):

│   ├── routes/              # API endpoints{

│   │   ├── auth.py         # Login, register, logout    "id": 1,

│   │   └── todo.py         # List/item CRUD operations    "username": "john_doe",

│   └── services/            # Business logic    "email": "john@example.com",

│       ├── auth.py         # Authentication service    "created_at": "2024-01-15T10:30:00"

│       └── permission.py   # Authorization checks}

├── models/                   # Database models (3NF)

│   ├── user.py             # User with password hashingError (400):

│   ├── todo_list.py        # Todo lists{

│   └── todo_item.py        # Hierarchical items (self-referential)    "error": "Username or email already exists"

├── frontend/                 # React TypeScript app}

│   ├── src/```

│   │   ├── components/     # Reusable UI components

│   │   ├── contexts/       # State management (Auth, Tasks)#### Login User

│   │   ├── pages/          # Login, Dashboard, ListPage```

│   │   ├── services/       # API integration layerPOST /api/auth/login

│   │   └── types/          # TypeScript interfacesContent-Type: application/json

│   └── package.json        # Node dependencies

├── instance/{

│   └── app.db              # SQLite database    "username": "john_doe",

├── run.py                   # Flask entry point    "password": "secure_password"

├── seed.py                  # Database seeder script}

├── config.py                # Flask configuration

├── requirements.txt         # Python dependenciesResponse (200):

├── .gitignore               # Git exclusions{

└── README.md                # This file    "id": 1,

```    "username": "john_doe",

    "email": "john@example.com"

---}



## 🎨 Features & User InterfaceError (401):

{

### Beautiful, Modern UI    "error": "Invalid credentials"

- **Gradient backgrounds** (blue → purple)}

- **Smooth animations** with Framer Motion```

- **Responsive design** (desktop + mobile)

- **Glassmorphism effects** on cards#### Get Current User

- **Toast notifications** for feedback```

- **Loading spinners** during operationsGET /api/auth/me



### Dashboard ViewResponse (200):

- Grid of all your todo lists{

- Click any list to view its tasks    "id": 1,

- Create new lists with sidebar button    "username": "john_doe",

- Beautiful empty states with helpful prompts    "email": "john@example.com",

    "created_at": "2024-01-15T10:30:00"

### List View (Hierarchical Tasks)}

- **Tree structure** showing parent-child relationships

- **Expand/collapse** - Click arrow to show/hide childrenError (401):

- **Complete tasks** - Click circle icon (turns green ✅){

- **Hover actions** - Edit ✏️, Delete 🗑️, Add subtask ➕    "error": "Not authenticated"

- **Visual depth** - Indentation shows hierarchy level}

- **Max 3 levels** - Items can have sub-items, which can have sub-sub-items```



### Task Management#### Logout User

- **Add tasks**: Click "Add Task" button```

- **Add subtasks**: Hover over task → click + icon (if not at max depth)POST /api/auth/logout

- **Edit tasks**: Hover → click edit icon → modify title/description

- **Delete tasks**: Hover → click trash → confirms before deleting (cascades to children)Response (200):

- **Mark complete**: Click checkbox (strikethrough + opacity change){

- **Collapse children**: Click arrow to hide subtasks    "message": "Logged out successfully"

}

---```



## 🗄️ Database Schema### TodoList Endpoints (`/api`)



### Tables (3NF Normalized)#### Create List

```

**USER**POST /api/lists

- `id` (PK)Content-Type: application/json

- `username` (UNIQUE INDEX)

- `email` (UNIQUE INDEX){

- `password_hash`    "title": "Shopping List",

- `created_at`, `updated_at`    "description": "Weekly groceries"

}

**TODOLIST**

- `id` (PK)Response (201):

- `user_id` (FK → USER, INDEX){

- `title`, `description`    "id": 1,

- `created_at`, `updated_at`    "title": "Shopping List",

    "description": "Weekly groceries",

**TODOITEM** (Hierarchical)    "user_id": 1,

- `id` (PK)    "created_at": "2024-01-15T10:30:00",

- `list_id` (FK → TODOLIST, INDEX)    "updated_at": "2024-01-15T10:30:00"

- `parent_id` (FK → TODOITEM, INDEX) *self-referential*}

- `title`, `description````

- `is_completed` (BOOLEAN, INDEX)

- `is_collapsed` (BOOLEAN, INDEX)#### Get All User Lists

- `order` (INTEGER, INDEX)```

- `created_at`, `updated_at`GET /api/lists



### RelationshipsResponse (200):

- User → TodoList (1:Many, CASCADE DELETE)[

- TodoList → TodoItem (1:Many, CASCADE DELETE)    {

- TodoItem → TodoItem (1:Many, CASCADE DELETE) *hierarchical*        "id": 1,

        "title": "Shopping List",

---        "description": "Weekly groceries",

        "user_id": 1,

## 🔌 API Endpoints        "created_at": "2024-01-15T10:30:00",

        "updated_at": "2024-01-15T10:30:00"

### Authentication (`/api/auth`)    },

- `POST /register` - Create new user account    ...

- `POST /login` - User login (creates session)]

- `POST /logout` - User logout```

- `GET /me` - Get current user info

#### Get List with Items

### Todo Lists (`/api`)```

- `GET /lists` - Get all user's listsGET /api/lists/{list_id}

- `POST /lists` - Create new list

- `GET /lists/<id>` - Get list with items (hierarchical)Response (200):

- `PUT /lists/<id>` - Update list{

- `DELETE /lists/<id>` - Delete list (and all items)    "id": 1,

    "title": "Shopping List",

### Todo Items (`/api`)    "description": "Weekly groceries",

- `POST /items` - Create item or subtask    "user_id": 1,

- `GET /items/<id>` - Get item with children    "created_at": "2024-01-15T10:30:00",

- `PUT /items/<id>` - Update item    "updated_at": "2024-01-15T10:30:00",

- `DELETE /items/<id>` - Delete item (and all descendants)    "items": [

- `PATCH /items/<id>/complete` - Toggle complete status        {

- `PATCH /items/<id>/collapse` - Toggle collapse status            "id": 1,

- `PATCH /items/<id>/move` - Move item to different list            "title": "Milk",

            "parent_id": null,

---            "is_completed": false,

            "is_collapsed": false,

## 🔒 Security & Data Isolation            "order": 0,

            "depth": 0,

- **Password hashing** using Werkzeug            "children": []

- **Session-based authentication** with secure cookies        },

- **CORS protection** (localhost only)        ...

- **Authorization checks** on every endpoint    ]

- **SQL injection protection** via SQLAlchemy ORM}

- **User data isolation** - Users cannot access others' data```



---#### Update List

```

## 🛠️ Technology StackPUT /api/lists/{list_id}

Content-Type: application/json

### Backend

- **Flask 3.0.0** - Web framework{

- **SQLAlchemy 3.1.1** - Database ORM    "title": "Updated Title",

- **Flask-CORS 4.0.0** - Cross-origin requests    "description": "Updated description"

- **SQLite** - Lightweight database}

- **Python 3.12** - Programming language

Response (200):

### Frontend{

- **React 18.2.0** - UI library    "id": 1,

- **TypeScript 5.2.2** - Type-safe JavaScript    "title": "Updated Title",

- **Vite 5.0.8** - Fast build tool    ...

- **Tailwind CSS 3.3.6** - Utility-first CSS}

- **Framer Motion 10.16.16** - Animations```

- **Axios 1.6.2** - HTTP client

- **React Router 6.20.0** - Navigation#### Delete List

```

---DELETE /api/lists/{list_id}



## 📝 Code DocumentationResponse (200):

{

### Python Code    "message": "List deleted"

- **Docstrings** on all classes and functions}

- **Type hints** where appropriate```

- **Inline comments** explaining complex logic

- **Service layer** separates business logic from routes### TodoItem Endpoints (`/api`)



### TypeScript Code#### Create Item

- **Interface definitions** for all data structures```

- **JSDoc comments** on complex componentsPOST /api/items

- **Type-safe** throughout (no `any` types)Content-Type: application/json

- **Component documentation** in headers

{

---    "list_id": 1,

    "parent_id": null,

## 🧪 Demo Data    "title": "Buy Milk",

    "description": "2% milk",

Run `python seed.py` to populate the database with:    "order": 0

}

**3 Demo Users:**

1. `john_doe` / `password123` - 3 lists with hierarchical itemsResponse (201):

2. `jane_smith` / `password123` - 2 lists{

3. `alice_wonder` / `password123` - 1 list    "id": 1,

    "list_id": 1,

**Sample Hierarchy (john_doe's Shopping List):**    "parent_id": null,

```    "title": "Buy Milk",

Shopping List    "description": "2% milk",

├── Produce    "is_completed": false,

│   ├── Buy 2kg Apples ✅    "is_collapsed": false,

│   │   └── Check if organic available    "order": 0,

│   ├── Buy Bananas    "depth": 0,

│   └── Buy Carrots    "created_at": "2024-01-15T10:30:00",

├── Dairy    "updated_at": "2024-01-15T10:30:00"

│   └── Buy Milk}

└── Snacks```

```

#### Create Sub-Item (Nested Task)

---```

POST /api/items

## ⚙️ ConfigurationContent-Type: application/json



### Environment Variables{

The app supports different configurations:    "list_id": 1,

- **Development** (default) - Debug mode ON    "parent_id": 1,

- **Production** - Debug mode OFF, optimized    "title": "Check 2% vs whole milk",

- **Testing** - In-memory database    "order": 0

}

### CORS Settings

Frontend origins allowed:Response (201):

- `http://localhost:3000`{

- `http://localhost:3001`    "id": 2,

    "list_id": 1,

---    "parent_id": 1,

    "title": "Check 2% vs whole milk",

## 🐛 Troubleshooting    "depth": 1,

    ...

### "Network error" on login}

**Solution**: Make sure Flask backend is running on port 5000

```bashError (400) - Max Depth Exceeded:

python run.py{

```    "error": "Maximum nesting depth (3 levels) reached"

}

### Frontend won't start```

**Solution**: Install dependencies and try different port

```bash#### Get Item with Children

npm install```

npm run devGET /api/items/{item_id}

```

Response (200):

### Database errors{

**Solution**: Reset database with seed script    "id": 1,

```bash    "title": "Buy Milk",

python seed.py    "parent_id": null,

```    "is_completed": false,

    "is_collapsed": false,

### Port already in use    "order": 0,

**Solution**: Vite will automatically try port 3001 if 3000 is busy    "depth": 0,

    "children": [

---        {

            "id": 2,

## 📋 Assignment Compliance            "title": "Check 2% vs whole milk",

            "parent_id": 1,

### Required Features            "is_completed": false,

✅ Multiple users with data isolation              "depth": 1,

✅ Authentication (no forgot password needed)              "children": []

✅ Mark tasks complete/incomplete          }

✅ Collapse/expand subtasks      ],

✅ Move top-level tasks between lists      "created_at": "2024-01-15T10:30:00",

✅ Durable storage (SQLite database)      "updated_at": "2024-01-15T10:30:00"

✅ Max 3-level hierarchy  }

✅ Hide/show subtasks feature  ```



### Submission Requirements#### Update Item

✅ Zip file with all code  ```

✅ requirements.txt for dependencies  PUT /api/items/{item_id}

✅ README.md with installation instructions  Content-Type: application/json

✅ Works with provided commands  

✅ Virtual environment excluded (.gitignore)  {

✅ Detailed code comments      "title": "Updated title",

⬜ **Screen recording demo** - ADD YOUR LINK!    "is_completed": true,

    "is_collapsed": false,

---    "order": 1

}

## 🎯 What Makes This Project Special

Response (200):

1. **Full-Stack TypeScript**: Type safety from database to UI{

2. **Modern UI/UX**: Beautiful animations and responsive design    "id": 1,

3. **3NF Database**: Properly normalized with strategic indexing    "title": "Updated title",

4. **Security First**: Password hashing, CORS, session management    "is_completed": true,

5. **Production-Ready**: Error handling, loading states, validation    ...

6. **Well-Documented**: Comprehensive README, inline comments, docstrings}

7. **Easy Setup**: One-command installation for both backend and frontend```



---#### Delete Item

```

## 🚀 Future EnhancementsDELETE /api/items/{item_id}



Potential improvements beyond MVP:Response (200):

- [ ] Drag-and-drop task reordering{

- [ ] Task due dates and priorities    "message": "Item deleted"

- [ ] Search and filter functionality}

- [ ] Dark mode toggle

- [ ] Email notificationsNote: Deleting an item cascades to all descendants

- [ ] Export tasks to JSON/CSV```

- [ ] Unit and integration tests

- [ ] Mobile app (React Native)#### Move Item to Different List

```

---PATCH /api/items/{item_id}/move

Content-Type: application/json

## 👨‍💻 Development Notes

{

### Windows Compatibility    "target_list_id": 2

- Werkzeug reloader disabled by default on Windows (prevents exit code 1 errors)}

- Use `FLASK_USE_RELOADER=1` environment variable to re-enable if needed

Response (200):

### Database Seeding{

- Safe to run `python seed.py` multiple times    "id": 1,

- Clears existing data before inserting new demo data    "list_id": 2,

- Creates realistic hierarchical structures for testing    ...

}

### Frontend-Backend Communication

- Vite dev server proxies `/api/*` requests to Flask backendError (400):

- Session cookies work with `credentials: true` in Axios{

- CORS configured to allow localhost origins    "error": "Can only move top-level items"

}

---```



## 📄 License## Security Features



Educational project for CS162 Assignment 2- **Session-Based Authentication**: User authentication via Flask sessions

- **Password Hashing**: werkzeug.security for secure password storage

---- **Permission Checks**: All endpoints verify user ownership of data

- **Data Isolation**: Users can only access their own lists and items

## 🙏 Acknowledgments- **CSRF Protection**: Session-based tokens prevent CSRF attacks

- **ACID Transactions**: Database transactions ensure consistency

- Built using Flask, React, TypeScript, and Tailwind CSS

- Animations powered by Framer Motion## Authentication Flow

- Icons from React Icons

1. User registers with unique username and email

---2. Password is hashed with salt using werkzeug

3. Login verifies credentials and creates session

**Last Updated**: November 1, 20254. Session ID stored in cookie

5. Each request verifies user owns the requested resource

**Remember to add your screen recording link at the top of this README!** 🎥6. Logout destroys session



## Hierarchical Todo Structure

The application supports up to 3 levels of task hierarchy:

```
Level 0 (Top-level)
├─ Level 1 (Subtask)
│  ├─ Level 2 (Sub-subtask)
│  │  └─ Cannot add Level 3 (max depth enforced)
│  └─ Level 2 (Sub-subtask)
└─ Level 1 (Subtask)
```

Each level can have multiple items, and each can be independently marked as completed or collapsed for UI rendering.

## Database Indices

### Single Column Indices
- `users.username` - Unique constraint, faster login
- `users.email` - Unique constraint, faster registration
- `users.created_at` - Sort users by registration date
- `todo_lists.user_id` - Fetch user's lists
- `todo_lists.created_at` - Sort lists by creation
- `todo_items.list_id` - Fetch items in a list
- `todo_items.parent_id` - Fetch children (critical for recursion)
- `todo_items.is_completed` - Filter active tasks
- `todo_items.is_collapsed` - UI rendering
- `todo_items.order` - Sort items

### Composite Indices
- `(todo_lists.user_id, created_at)` - User lists sorted
- `(todo_items.list_id, parent_id)` - Items with hierarchy
- `(todo_items.parent_id, order)` - Sorted children
- `(todo_items.parent_id, is_collapsed, order)` - Visible items
- `(todo_items.parent_id, is_completed)` - Active subtasks

## Error Handling

All errors return JSON with appropriate HTTP status codes:

- **400 Bad Request** - Invalid input or missing fields
- **401 Unauthorized** - User not authenticated
- **403 Forbidden** - User does not own resource
- **404 Not Found** - Resource doesn't exist
- **500 Internal Server Error** - Database or server error

## Environment Configuration

### Development
```
Debug: Enabled
Database: SQLite (dev.db)
Session: In-memory
```

### Production
```
Debug: Disabled
Database: Configure in config.py
Session: Secure cookies only
SQLALCHEMY_ECHO: Disabled
```

### Testing
```
Debug: Enabled
Database: In-memory SQLite
Session: Testing mode
```

## Extension Points

### Adding New Authentication Strategies

The Strategy pattern makes it easy to add new auth methods:

```python
class OAuthStrategy(AuthenticationStrategy):
    def authenticate(self, **kwargs):
        # OAuth implementation
        pass

# Use it
auth_service.set_strategy(OAuthStrategy())
```

### Adding New Business Logic

Create new services following the pattern in `app/services/`:

```python
class NotificationService:
    @staticmethod
    def notify_task_completed(user_id, task_title):
        # Send notification
        pass
```

## Performance Considerations

- Lazy loading relationships avoid N+1 queries
- Composite indices optimize recursive queries
- Session-based caching reduces password hashing overhead
- Explicit query optimization with `lazy='select'`

## Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` environment variable
2. Configure database URL in `config.py`
3. Use production WSGI server (Gunicorn, uWSGI)
4. Enable HTTPS/TLS
5. Configure CORS if using separate frontend

## Future Enhancements (Phase 2-3)

- React frontend with responsive UI
- Real-time updates with WebSockets
- Task categories and tags
- Due dates and reminders
- Sharing lists with other users
- Cloud storage integration
- Mobile app support
- Dark mode and themes

## Contributing

Code follows PEP 8 standards with these conventions:

- Type hints for function parameters
- Docstrings for all public methods
- Comprehensive error handling
- Security-first approach
- Test coverage for critical paths

## License

This project is submitted for CS162 Web Application course review.

## Author

CS162 Web Application Assignment - Hierarchical Todo List

## Support

For issues or questions, refer to the DATABASE_SCHEMA.md for detailed database design documentation.
