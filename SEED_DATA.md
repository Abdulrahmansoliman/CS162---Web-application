# Database Seeding

This directory contains a seeding script to populate the database with dummy data for testing and development.

## Quick Start

### 1. Ensure the app is properly configured
Make sure `config.py` is set up and `models/` are defined.

### 2. Run the seed script
```bash
python seed.py
```

### 3. Expected Output
```
🗑️  Clearing existing data...
👤 Creating users...
✅ Created 3 users: john_doe, jane_smith, bob_wilson

📋 Creating todo lists for john_doe...
✅ Created 3 lists for john_doe

🛒 Adding items to Shopping List...
✅ Added 10 hierarchical items to Shopping List

💼 Adding items to Work Projects...
✅ Added 5 hierarchical items to Work Projects

🏠 Adding items to Home Maintenance...
✅ Added 3 items to Home Maintenance

📋 Creating todo lists for jane_smith...
✅ Created 2 lists for jane_smith with 5 items

📋 Creating todo lists for bob_wilson...
✅ Created 1 list for bob_wilson with 3 items

==================================================
✅ DATABASE SEEDING COMPLETE!
==================================================

📊 Summary:
   Users created: 3
   Todo lists created: 6
   Todo items created: 26

🔐 Test Credentials:
   1. john_doe / password123
   2. jane_smith / password456
   3. bob_wilson / password789

🚀 Next steps:
   1. Run: python run.py
   2. Open: http://localhost:5000
   3. Login with any test account above
```

## What Gets Created

### Users (3 total)
- **john_doe** (password123) - Has 3 lists with complex hierarchical items
- **jane_smith** (password456) - Has 2 lists with personal goals
- **bob_wilson** (password789) - Has 1 list with development tasks

### Todo Lists (6 total)

**For john_doe:**
1. **Shopping List** (10 hierarchical items)
   - Produce (with Apples → details, Bananas, Carrots)
   - Dairy (Milk, Cheese, Yogurt)
   - Meat & Protein
   - Snacks

2. **Work Projects** (5 hierarchical items)
   - Project Alpha → Design → Wireframes, Prototype
   - Project Beta

3. **Home Maintenance** (3 items)
   - Clean kitchen
   - Fix leaky faucet
   - Mow the lawn

**For jane_smith:**
1. **Personal Goals** (3 items)
   - Learn Python
   - Read 12 books this year
   - Plan Europe trip

2. **Fitness Plan** (2 items)
   - Gym workouts
   - Running routine

**For bob_wilson:**
1. **Development Tasks** (3 items)
   - Fix critical bugs
   - Code review PR #42
   - Write API documentation

### Todo Items (26 total)
- 3 levels of nesting (max depth constraint)
- Mixed completion states (some marked complete)
- Realistic descriptions for testing
- Order field populated for sorting

## Testing with Seed Data

After seeding, you can:

1. **Test User Authentication**
   - Try logging in with different users
   - Verify session creation

2. **Test Data Isolation**
   - Login as john_doe → See only john_doe's lists
   - Logout and login as jane_smith → See only jane_smith's lists
   - Cannot access other users' data

3. **Test Hierarchical Queries**
   - GET `/api/lists/1` → Returns shopping list with all items
   - See items organized in 3-level hierarchy
   - Test collapse/expand functionality

4. **Test CRUD Operations**
   - Create new items
   - Update existing items
   - Delete items (test cascading)
   - Move items between lists

5. **Test Permission Checks**
   - Try accessing another user's list → 403 Forbidden
   - Try deleting someone else's item → 403 Forbidden

## Reset Database

To clear and reseed:
```bash
# Simply run seed.py again - it clears old data first
python seed.py
```

## Notes

- The seed script creates an SQLite database at `./dev.db` if it doesn't exist
- Running seed.py multiple times will reset to the same initial state
- All passwords are hashed using werkzeug.security (not stored as plaintext)
- Timestamps are set to current time during seeding
