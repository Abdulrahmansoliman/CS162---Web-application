# Hierarchical Todo List Web Application

A professional-grade web application for managing hierarchical todo lists with user authentication and data isolation. Built with Flask backend and SQLAlchemy ORM using 3NF database normalization.

## Architecture Overview

### Design Patterns

- **Strategy Pattern**: Authentication system supports multiple authentication strategies (local, OAuth, LDAP, etc.) without code changes
- **Factory Pattern**: Application factory allows creation of different app instances for different environments
- **Service Layer**: Centralized business logic in services (auth, permissions) for easy testing and reusability
- **Blueprint Pattern**: Flask blueprints organize routes by domain (auth, todo)

### Database Design

- **3NF Normalization**: Ensures data integrity and eliminates redundancy
- **ACID Compliance**: All transactions maintain Atomicity, Consistency, Isolation, Durability
- **Strategic Indexing**: 10 single + 4 composite indices optimize query performance
- **Cascading Deletes**: Maintain referential integrity when deleting users, lists, or items
- **Hierarchical Support**: Self-referential TodoItem with max 3-level depth constraint

### Key Technologies

- **Backend**: Flask 3.0.0 + Flask-SQLAlchemy 3.1.1
- **Database**: SQLite (easily migrates to PostgreSQL)
- **Authentication**: Session-based with werkzeug password hashing
- **Configuration**: Environment-based (Development, Production, Testing)

## Project Structure

```
├── app/
│   ├── __init__.py           # Application factory
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── todo.py          # TodoList & TodoItem endpoints
│   └── services/
│       ├── auth.py          # Authentication service (Strategy pattern)
│       ├── permission.py    # Authorization & access control
│       └── __init__.py      # Service exports
├── models/
│   ├── __init__.py          # SQLAlchemy initialization
│   ├── user.py              # User model
│   ├── todo_list.py         # TodoList model
│   └── todo_item.py         # TodoItem model (hierarchical)
├── config.py                 # Configuration for environments
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── DATABASE_SCHEMA.md        # ER diagram and schema docs
└── README.md                 # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Application

**Development Mode** (with auto-reload and debug):
```bash
python run.py
```

**Production Mode**:
```bash
set FLASK_ENV=production
python run.py
```

The server runs on `http://localhost:5000`

### 3. Database

The application automatically creates the SQLite database on first run. Database file is created at the project root as `dev.db`.

## API Documentation

All endpoints return JSON responses. Authentication uses session-based cookies.

### Authentication Endpoints (`/api/auth`)

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

Error (400):
{
    "error": "Username or email already exists"
}
```

#### Login User
```
POST /api/auth/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password"
}

Response (200):
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
}

Error (401):
{
    "error": "Invalid credentials"
}
```

#### Get Current User
```
GET /api/auth/me

Response (200):
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00"
}

Error (401):
{
    "error": "Not authenticated"
}
```

#### Logout User
```
POST /api/auth/logout

Response (200):
{
    "message": "Logged out successfully"
}
```

### TodoList Endpoints (`/api`)

#### Create List
```
POST /api/lists
Content-Type: application/json

{
    "title": "Shopping List",
    "description": "Weekly groceries"
}

Response (201):
{
    "id": 1,
    "title": "Shopping List",
    "description": "Weekly groceries",
    "user_id": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
}
```

#### Get All User Lists
```
GET /api/lists

Response (200):
[
    {
        "id": 1,
        "title": "Shopping List",
        "description": "Weekly groceries",
        "user_id": 1,
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
    },
    ...
]
```

#### Get List with Items
```
GET /api/lists/{list_id}

Response (200):
{
    "id": 1,
    "title": "Shopping List",
    "description": "Weekly groceries",
    "user_id": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "items": [
        {
            "id": 1,
            "title": "Milk",
            "parent_id": null,
            "is_completed": false,
            "is_collapsed": false,
            "order": 0,
            "depth": 0,
            "children": []
        },
        ...
    ]
}
```

#### Update List
```
PUT /api/lists/{list_id}
Content-Type: application/json

{
    "title": "Updated Title",
    "description": "Updated description"
}

Response (200):
{
    "id": 1,
    "title": "Updated Title",
    ...
}
```

#### Delete List
```
DELETE /api/lists/{list_id}

Response (200):
{
    "message": "List deleted"
}
```

### TodoItem Endpoints (`/api`)

#### Create Item
```
POST /api/items
Content-Type: application/json

{
    "list_id": 1,
    "parent_id": null,
    "title": "Buy Milk",
    "description": "2% milk",
    "order": 0
}

Response (201):
{
    "id": 1,
    "list_id": 1,
    "parent_id": null,
    "title": "Buy Milk",
    "description": "2% milk",
    "is_completed": false,
    "is_collapsed": false,
    "order": 0,
    "depth": 0,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
}
```

#### Create Sub-Item (Nested Task)
```
POST /api/items
Content-Type: application/json

{
    "list_id": 1,
    "parent_id": 1,
    "title": "Check 2% vs whole milk",
    "order": 0
}

Response (201):
{
    "id": 2,
    "list_id": 1,
    "parent_id": 1,
    "title": "Check 2% vs whole milk",
    "depth": 1,
    ...
}

Error (400) - Max Depth Exceeded:
{
    "error": "Maximum nesting depth (3 levels) reached"
}
```

#### Get Item with Children
```
GET /api/items/{item_id}

Response (200):
{
    "id": 1,
    "title": "Buy Milk",
    "parent_id": null,
    "is_completed": false,
    "is_collapsed": false,
    "order": 0,
    "depth": 0,
    "children": [
        {
            "id": 2,
            "title": "Check 2% vs whole milk",
            "parent_id": 1,
            "is_completed": false,
            "depth": 1,
            "children": []
        }
    ],
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
}
```

#### Update Item
```
PUT /api/items/{item_id}
Content-Type: application/json

{
    "title": "Updated title",
    "is_completed": true,
    "is_collapsed": false,
    "order": 1
}

Response (200):
{
    "id": 1,
    "title": "Updated title",
    "is_completed": true,
    ...
}
```

#### Delete Item
```
DELETE /api/items/{item_id}

Response (200):
{
    "message": "Item deleted"
}

Note: Deleting an item cascades to all descendants
```

#### Move Item to Different List
```
PATCH /api/items/{item_id}/move
Content-Type: application/json

{
    "target_list_id": 2
}

Response (200):
{
    "id": 1,
    "list_id": 2,
    ...
}

Error (400):
{
    "error": "Can only move top-level items"
}
```

## Security Features

- **Session-Based Authentication**: User authentication via Flask sessions
- **Password Hashing**: werkzeug.security for secure password storage
- **Permission Checks**: All endpoints verify user ownership of data
- **Data Isolation**: Users can only access their own lists and items
- **CSRF Protection**: Session-based tokens prevent CSRF attacks
- **ACID Transactions**: Database transactions ensure consistency

## Authentication Flow

1. User registers with unique username and email
2. Password is hashed with salt using werkzeug
3. Login verifies credentials and creates session
4. Session ID stored in cookie
5. Each request verifies user owns the requested resource
6. Logout destroys session

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
