# Hierarchical Todo List Application

A full-stack web application for managing hierarchical todo lists with infinite nesting, drag-and-drop, priorities, and real-time progress tracking.

## 🎯 Project Overview

This application demonstrates professional software engineering principles including:
- **Object-Oriented Programming (OOP)** concepts
- **Design Patterns** (Strategy, Facade, Active Record)
- **SOLID Principles** (Single Responsibility, Open/Closed, etc.)
- **Clean Architecture** with clear separation of concerns

---

## 📋 Features

### Core Features (MVP)
- ✅ **Multi-user authentication** - Secure registration and login
- ✅ **User data isolation** - Each user sees only their own tasks
- ✅ **Mark tasks complete** - Track completion with automatic parent chain updates
- ✅ **Collapse/expand tasks** - Hide subtasks to focus on important items
- ✅ **Move tasks between lists** - Reorganize top-level tasks across lists
- ✅ **Durable storage** - SQLite database with proper 3NF normalization

### Extended Features
- ✅ **Infinite nesting** - No depth limit on subtasks
- ✅ **Drag-and-drop** - Reorder tasks with visual feedback
- ✅ **Priority system** - 4 levels (Low, Medium, High, Urgent)
- ✅ **Progress tracking** - Visual progress bars on dashboard
- ✅ **Depth indicators** - Color-coded badges showing nesting level
- ✅ **Bulk operations** - Mark all tasks in a list complete at once
- ✅ **Smart completion** - Auto-complete parents when all children done

---

## 🏗️ Architecture & Design Principles

### Backend Architecture

```
app/
├── routes/          # HTTP request handlers (thin layer)
│   ├── auth.py      # Authentication routes
│   └── todo.py      # Todo list/item routes
├── services/        # Business logic layer (CORE)
│   ├── auth.py      # Authentication service (Strategy pattern)
│   ├── permission.py # Authorization service
│   ├── todo_service.py # Todo business logic
│   └── validators.py # Request validation helpers
└── models/          # Database models (Active Record pattern)
    ├── user.py      # User model
    ├── todo_list.py # TodoList model
    └── todo_item.py # TodoItem model (hierarchical)
```

### Frontend Architecture

```
frontend/src/
├── components/
│   ├── common/      # Reusable UI components
│   ├── layout/      # Layout components (Header, Sidebar)
│   └── tasks/       # Task-specific components (MODULAR)
│       ├── TaskItem.tsx            # Main task component
│       ├── TaskActionButtons.tsx   # Action button group (SRP)
│       ├── TaskItemModals.tsx      # All modals (SRP)
│       ├── PriorityBadge.tsx       # Priority display (ABSTRACTION)
│       ├── DepthBadge.tsx          # Depth indicator (ABSTRACTION)
│       ├── PrioritySelector.tsx    # Priority selection UI (REUSABLE)
│       ├── taskUtils.ts            # Utility functions (PURE)
│       └── useTaskItemLogic.ts     # Business logic hook (SRP)
├── contexts/        # React Context for global state
├── pages/           # Page components
└── services/        # API client layer
```

---

## 🎨 OOP Principles Demonstrated

### 1. **Single Responsibility Principle (SRP)**

**Problem Before**: `TaskItem.tsx` had 614 lines doing everything:
- Rendering UI
- Managing state
- Handling API calls
- Modal logic
- Form validation

**Solution**: Split into 7 focused components:

```typescript
// ❌ BEFORE: One giant component doing everything
TaskItem.tsx (614 lines)

// ✅ AFTER: Each component has ONE job
TaskItem.tsx          // Main component (orchestration)
TaskActionButtons.tsx // ONLY renders action buttons
TaskItemModals.tsx    // ONLY handles modal UI
PriorityBadge.tsx     // ONLY displays priority
DepthBadge.tsx        // ONLY shows depth level
PrioritySelector.tsx  // ONLY handles priority selection
useTaskItemLogic.ts   // ONLY manages business logic
taskUtils.ts          // ONLY provides utility functions
```

**Backend Example**:
```python
# ❌ BEFORE: Routes doing everything
@app.route('/items', methods=['POST'])
def create_item():
    # Validation logic
    # Permission checking
    # Business logic
    # Database operations
    # Parent chain updates
    # 80 lines of mixed concerns

# ✅ AFTER: Routes delegate to services
@app.route('/items', methods=['POST'])
def create_item():
    # Just HTTP handling + delegation (20 lines)
    return TodoItemService.create_item(...)
```

### 2. **Abstraction**

**Hiding Complexity**:
```typescript
// ❌ BEFORE: Component needs to know indentation algorithm
const indentation = level === 0 ? 0 
  : level <= 3 ? level * 24 
  : 72 + ((level - 3) * 12);

// ✅ AFTER: Simple function call, complexity hidden
import { calculateIndentation } from './taskUtils';
const indentation = calculateIndentation(level);
```

**Backend Abstraction**:
```python
# ❌ BEFORE: Routes know database details
item = TodoItem(list_id=list_id, title=title, ...)
db.session.add(item)
if parent_id:
    parent = TodoItem.query.get(parent_id)
    if parent.is_completed:
        parent.uncomplete_parent_chain()
db.session.commit()

# ✅ AFTER: Simple service call
item = TodoItemService.create_item(
    list_id=list_id, 
    title=title
)
```

### 3. **Polymorphism**

**Strategy Pattern in Authentication**:
```python
class AuthenticationStrategy(ABC):
    """Abstract base class - defines interface"""
    @abstractmethod
    def authenticate(self, **kwargs):
        pass

class LocalAuthStrategy(AuthenticationStrategy):
    """Concrete strategy for local auth"""
    def authenticate(self, username, password):
        # Implementation

class OAuthStrategy(AuthenticationStrategy):
    """Different implementation, same interface"""
    def authenticate(self, token):
        # Different implementation

# POLYMORPHISM: Can swap strategies without changing code
auth_service = AuthenticationService(LocalAuthStrategy())
# Later: auth_service.set_strategy(OAuthStrategy())
```

### 4. **Encapsulation**

**Backend Models**:
```python
class TodoItem(db.Model):
    # PRIVATE data (accessed via methods)
    id = db.Column(...)
    is_completed = db.Column(...)
    
    # PUBLIC interface
    def can_be_completed(self):
        """Encapsulates completion logic"""
        return all(child.is_completed for child in self.children)
    
    def auto_complete_parent_chain(self):
        """Hides complex parent chain logic"""
        # Implementation hidden from callers
```

### 5. **Modularity**

**Before**: Monolithic components
**After**: Composable, reusable pieces

```typescript
// Modular composition
<TaskItem>
  <DepthBadge level={level} />
  <PriorityBadge priority={item.priority} onCycle={...} />
  <TaskActionButtons 
    canAddChild={true}
    onAddChild={openAddModal}
    onEdit={openEditModal}
    onDelete={handleDelete}
  />
  <TaskItemModals {...modalProps} />
</TaskItem>
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to project folder
cd "CS162---Web-application"

# Activate your conda environment (if using conda)
conda activate sage

# Or create virtual environment (if not using conda)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Seed database with demo data
python seed.py

# Run backend server
python run.py
```

Backend runs on: `http://127.0.0.1:5000`

### Frontend Setup

Open a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on: `http://localhost:3001`

### Access the Application

1. Open browser to `http://localhost:3001`
2. Login with demo account:
   - Username: `john_doe`
   - Password: `password123`
3. Explore your todo lists!

---

## 📁 Code Structure Explained

### Backend Layer Responsibilities

#### 1. **Routes Layer** (`app/routes/`)
**Responsibility**: Handle HTTP requests/responses ONLY
- Receive HTTP requests
- Validate input
- Check permissions
- Delegate to services
- Return HTTP responses

#### 2. **Service Layer** (`app/services/`)
**Responsibility**: Business logic ONLY
- Create/update/delete operations
- Complex business rules
- Parent chain management
- Validation logic

#### 3. **Model Layer** (`models/`)
**Responsibility**: Data structure + relationships
- Define database schema
- Define relationships
- Provide data transformation (to_dict)
- Simple instance methods

#### 4. **Permission Layer** (`app/services/permission.py`)
**Responsibility**: Authorization ONLY
- Check if user owns resources
- Filter data by user
- Prevent unauthorized access

### Frontend Layer Responsibilities

#### 1. **Components** (`components/`)
**Responsibility**: UI rendering ONLY
- Display data
- Capture user input
- Delegate events to handlers

#### 2. **Hooks** (`useTaskItemLogic.ts`)
**Responsibility**: Component logic ONLY
- State management
- Event handlers
- Side effects

#### 3. **Services** (`services/`)
**Responsibility**: API communication ONLY
- HTTP requests
- Response parsing
- Error handling

#### 4. **Context** (`contexts/`)
**Responsibility**: Global state ONLY
- Shared state
- State updates
- Coordination between components

---

## 🧪 Testing (TODO - Bonus Points)

To implement unit tests for +4 bonus:

### Backend Tests (pytest)
```python
# tests/test_services.py
def test_create_item_validates_parent():
    error = TodoItemService.validate_parent(999, 1)
    assert error == 'Parent item not found'

def test_permission_check():
    assert not PermissionService.owns_list(list_id=1)  # Not logged in
```

### Frontend Tests (Jest)
```typescript
// taskUtils.test.ts
test('calculateIndentation returns correct values', () => {
  expect(calculateIndentation(0)).toBe(0);
  expect(calculateIndentation(1)).toBe(24);
  expect(calculateIndentation(4)).toBe(84);
});
```

---

## 📊 Database Schema

### Users Table
- `id` (PK)
- `username` (unique)
- `email` (unique)
- `password_hash`
- `created_at`

### TodoLists Table
- `id` (PK)
- `user_id` (FK → users.id)
- `title`
- `description`
- `created_at`

### TodoItems Table (Self-Referential)
- `id` (PK)
- `list_id` (FK → todo_lists.id)
- `parent_id` (FK → todo_items.id, nullable)
- `title`
- `description`
- `is_completed`
- `is_collapsed`
- `priority` (low/medium/high/urgent)
- `order` (for sorting)
- `created_at`

**Relationships**:
- User → TodoList (one-to-many)
- TodoList → TodoItem (one-to-many)
- TodoItem → TodoItem (self-referential, infinite nesting)

---

## 🎥 Demo Video

**[INSERT YOUR LOOM/VIDEO LINK HERE]**

**Demo includes**:
1. User registration/login
2. Creating lists and tasks
3. Adding nested subtasks (infinite depth)
4. Marking tasks complete (auto-complete demo)
5. Collapsing/expanding subtasks
6. Changing priorities (badge cycling)
7. Moving tasks between lists
8. Drag-and-drop reordering
9. Mark all complete feature
10. Deleting lists with confirmation

---

## 💡 Key Takeaways

### What I Learned

1. **SRP makes code maintainable**: Breaking `TaskItem.tsx` from 614 lines to 7 focused files made it much easier to understand and modify.

2. **Abstraction reduces complexity**: Utility functions like `calculateIndentation()` hide complexity and make code readable.

3. **Service layer is crucial**: Separating business logic from routes makes code testable and reusable.

4. **Comments matter**: Explaining WHY (not just what) helps future developers understand design decisions.

5. **Polymorphism enables flexibility**: Strategy pattern allows swapping authentication methods without changing code.

### Design Decisions

**Why infinite nesting?**
- Real-world projects often need more than 3 levels
- Shows understanding of recursive data structures

**Why service layer?**
- Testability without HTTP layer
- Reusable from CLI, background jobs, etc.
- Separates business logic from HTTP concerns

**Why component splitting?**
- Each component has clear purpose
- Easier to test individual pieces
- Components can be reused elsewhere

---

## 🚀 Technologies Used

### Backend
- **Flask** 3.0.0 - Web framework
- **SQLAlchemy** 3.1.1 - ORM
- **SQLite** - Database
- **Flask-Session** - Session management
- **Werkzeug** - Password hashing

### Frontend
- **React** 18.2.0 - UI framework
- **TypeScript** 4.9.5 - Type safety
- **Vite** 5.4.21 - Build tool
- **Tailwind CSS** 3.3.3 - Styling
- **Framer Motion** 10.16.4 - Animations
- **@hello-pangea/dnd** 16.5.0 - Drag-and-drop
- **React Router** 6.20.1 - Navigation

---

## 📝 Assignment Compliance

### MVP Requirements ✅
- [x] Multiple users with authentication
- [x] User data isolation (permission checks on every route)
- [x] Mark tasks complete
- [x] Collapse/expand tasks
- [x] Move top-level tasks between lists
- [x] Durable storage (SQLite database)

### Extensions ✅
- [x] Infinite nesting (no depth limit)
- [x] Arbitrary task movement (drag-and-drop)
- [ ] Unit tests (TODO for +4 bonus)

### Code Quality ✅
- [x] Clear README with installation instructions
- [x] Detailed code comments explaining OOP concepts
- [x] Well-organized project structure
- [x] Separation of concerns
- [x] SOLID principles applied

---

## 👨‍💻 Author

**Course**: CS162 - Web Application Development  
**Assignment**: Hierarchical Todo List  
**Date**: November 2025

---

## 📄 License

This project is created for educational purposes as part of CS162 coursework.
