"""
Database seeding script
Populates the database with dummy data for testing and demonstration
Run with: python seed.py
"""

from app import create_app, db
from models import User, TodoList, TodoItem


def seed_database():
    """Seed database with demo users, lists, and hierarchical items"""
    
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
        print("🗑️  Clearing existing data...")
        db.session.query(TodoItem).delete()
        db.session.query(TodoList).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create demo users
        print("👤 Creating users...")
        user1 = User(
            username='john_doe',
            email='john@example.com'
        )
        user1.set_password('password123')
        
        user2 = User(
            username='jane_smith',
            email='jane@example.com'
        )
        user2.set_password('password456')
        
        user3 = User(
            username='bob_wilson',
            email='bob@example.com'
        )
        user3.set_password('password789')
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        print(f"✅ Created 3 users: john_doe, jane_smith, bob_wilson")
        
        # Create lists for user1 (John)
        print("\n📋 Creating todo lists for john_doe...")
        shopping_list = TodoList(
            user_id=user1.id,
            title='Shopping List',
            description='Weekly grocery shopping'
        )
        work_list = TodoList(
            user_id=user1.id,
            title='Work Projects',
            description='Current work tasks and deadlines'
        )
        home_list = TodoList(
            user_id=user1.id,
            title='Home Maintenance',
            description='House repairs and cleaning'
        )
        
        db.session.add_all([shopping_list, work_list, home_list])
        db.session.commit()
        print(f"✅ Created 3 lists for john_doe")
        
        # Create hierarchical items for Shopping List
        print("\n🛒 Adding items to Shopping List...")
        
        # Top level: Categories
        produce = TodoItem(
            list_id=shopping_list.id,
            title='Produce',
            description='Fresh fruits and vegetables',
            order=0,
            is_completed=False
        )
        dairy = TodoItem(
            list_id=shopping_list.id,
            title='Dairy',
            description='Milk, cheese, yogurt',
            order=1,
            is_completed=False
        )
        meat = TodoItem(
            list_id=shopping_list.id,
            title='Meat & Protein',
            description='Chicken, beef, fish',
            order=2,
            is_completed=True
        )
        snacks = TodoItem(
            list_id=shopping_list.id,
            title='Snacks',
            description='Chips, nuts, candy',
            order=3,
            is_completed=False
        )
        
        db.session.add_all([produce, dairy, meat, snacks])
        db.session.commit()
        
        # Second level: Specific items under Produce
        apples = TodoItem(
            list_id=shopping_list.id,
            parent_id=produce.id,
            title='Buy 2kg Apples',
            description='Red apples preferred',
            order=0,
            is_completed=True
        )
        bananas = TodoItem(
            list_id=shopping_list.id,
            parent_id=produce.id,
            title='Buy Bananas',
            description='1 bunch',
            order=1,
            is_completed=False
        )
        carrots = TodoItem(
            list_id=shopping_list.id,
            parent_id=produce.id,
            title='Buy Carrots',
            description='1kg bag',
            order=2,
            is_completed=False
        )
        
        db.session.add_all([apples, bananas, carrots])
        db.session.commit()
        
        # Third level: Details for Apples
        check_price = TodoItem(
            list_id=shopping_list.id,
            parent_id=apples.id,
            title='Check if organic available',
            description='Prefer organic if available',
            order=0,
            is_completed=False
        )
        compare_stores = TodoItem(
            list_id=shopping_list.id,
            parent_id=apples.id,
            title='Compare prices at 3 stores',
            description='Find best price',
            order=1,
            is_completed=True
        )
        
        db.session.add_all([check_price, compare_stores])
        db.session.commit()
        
        # Items under Dairy
        milk = TodoItem(
            list_id=shopping_list.id,
            parent_id=dairy.id,
            title='Buy 2L Milk',
            description='2% reduced fat',
            order=0,
            is_completed=False
        )
        cheese = TodoItem(
            list_id=shopping_list.id,
            parent_id=dairy.id,
            title='Buy Cheddar Cheese',
            description='500g block',
            order=1,
            is_completed=False
        )
        yogurt = TodoItem(
            list_id=shopping_list.id,
            parent_id=dairy.id,
            title='Buy Greek Yogurt',
            description='Plain, 1kg container',
            order=2,
            is_completed=True
        )
        
        db.session.add_all([milk, cheese, yogurt])
        db.session.commit()
        
        print(f"✅ Added 10 hierarchical items to Shopping List")
        
        # Create hierarchical items for Work Projects
        print("\n💼 Adding items to Work Projects...")
        
        project_a = TodoItem(
            list_id=work_list.id,
            title='Project Alpha',
            description='Major client project',
            order=0,
            is_completed=False
        )
        project_b = TodoItem(
            list_id=work_list.id,
            title='Project Beta',
            description='Internal tools',
            order=1,
            is_completed=True
        )
        
        db.session.add_all([project_a, project_b])
        db.session.commit()
        
        # Tasks for Project Alpha
        design = TodoItem(
            list_id=work_list.id,
            parent_id=project_a.id,
            title='Design Phase',
            description='UI/UX mockups',
            order=0,
            is_completed=False
        )
        development = TodoItem(
            list_id=work_list.id,
            parent_id=project_a.id,
            title='Development',
            description='Frontend and backend',
            order=1,
            is_completed=False
        )
        
        db.session.add_all([design, development])
        db.session.commit()
        
        # Subtasks for Design
        wireframes = TodoItem(
            list_id=work_list.id,
            parent_id=design.id,
            title='Create wireframes',
            description='Mobile and desktop',
            order=0,
            is_completed=True
        )
        prototype = TodoItem(
            list_id=work_list.id,
            parent_id=design.id,
            title='Build interactive prototype',
            description='Using Figma',
            order=1,
            is_completed=False
        )
        
        db.session.add_all([wireframes, prototype])
        db.session.commit()
        
        print(f"✅ Added 5 hierarchical items to Work Projects")
        
        # Create simple items for Home Maintenance
        print("\n🏠 Adding items to Home Maintenance...")
        
        cleaning = TodoItem(
            list_id=home_list.id,
            title='Clean kitchen',
            description='Wipe counters and appliances',
            order=0,
            is_completed=False
        )
        repairs = TodoItem(
            list_id=home_list.id,
            title='Fix leaky faucet',
            description='Bathroom sink',
            order=1,
            is_completed=False
        )
        yard = TodoItem(
            list_id=home_list.id,
            title='Mow the lawn',
            description='Front and back',
            order=2,
            is_completed=True
        )
        
        db.session.add_all([cleaning, repairs, yard])
        db.session.commit()
        
        print(f"✅ Added 3 items to Home Maintenance")
        
        # Create lists for user2 (Jane)
        print("\n📋 Creating todo lists for jane_smith...")
        personal_list = TodoList(
            user_id=user2.id,
            title='Personal Goals',
            description='Learning and self-improvement'
        )
        fitness_list = TodoList(
            user_id=user2.id,
            title='Fitness Plan',
            description='Exercise and health tracking'
        )
        
        db.session.add_all([personal_list, fitness_list])
        db.session.commit()
        
        # Items for Personal Goals
        learn_python = TodoItem(
            list_id=personal_list.id,
            title='Learn Python',
            description='Complete online course',
            order=0,
            is_completed=False
        )
        read_books = TodoItem(
            list_id=personal_list.id,
            title='Read 12 books this year',
            description='One per month',
            order=1,
            is_completed=True
        )
        travel = TodoItem(
            list_id=personal_list.id,
            title='Plan Europe trip',
            description='Visit 5 countries',
            order=2,
            is_completed=False
        )
        
        db.session.add_all([learn_python, read_books, travel])
        db.session.commit()
        
        # Items for Fitness Plan
        gym = TodoItem(
            list_id=fitness_list.id,
            title='Gym workouts',
            description='4 times per week',
            order=0,
            is_completed=False
        )
        running = TodoItem(
            list_id=fitness_list.id,
            title='Running routine',
            description='3km runs on weekends',
            order=1,
            is_completed=True
        )
        
        db.session.add_all([gym, running])
        db.session.commit()
        
        print(f"✅ Created 2 lists for jane_smith with 5 items")
        
        # Create lists for user3 (Bob)
        print("\n📋 Creating todo lists for bob_wilson...")
        development_list = TodoList(
            user_id=user3.id,
            title='Development Tasks',
            description='Programming and coding'
        )
        
        db.session.add(development_list)
        db.session.commit()
        
        # Items for Development
        bug_fixes = TodoItem(
            list_id=development_list.id,
            title='Fix critical bugs',
            description='Priority: High',
            order=0,
            is_completed=False
        )
        code_review = TodoItem(
            list_id=development_list.id,
            title='Code review PR #42',
            description='3 pending reviews',
            order=1,
            is_completed=False
        )
        documentation = TodoItem(
            list_id=development_list.id,
            title='Write API documentation',
            description='Update all endpoints',
            order=2,
            is_completed=True
        )
        
        db.session.add_all([bug_fixes, code_review, documentation])
        db.session.commit()
        
        print(f"✅ Created 1 list for bob_wilson with 3 items")
        
        # Print summary
        print("\n" + "="*50)
        print("✅ DATABASE SEEDING COMPLETE!")
        print("="*50)
        
        user_count = db.session.query(User).count()
        list_count = db.session.query(TodoList).count()
        item_count = db.session.query(TodoItem).count()
        
        print(f"\n📊 Summary:")
        print(f"   Users created: {user_count}")
        print(f"   Todo lists created: {list_count}")
        print(f"   Todo items created: {item_count}")
        
        print(f"\n🔐 Test Credentials:")
        print(f"   1. john_doe / password123")
        print(f"   2. jane_smith / password456")
        print(f"   3. bob_wilson / password789")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Run: python app.py")
        print(f"   2. Open: http://localhost:5000")
        print(f"   3. Login with any test account above")


if __name__ == '__main__':
    try:
        seed_database()
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
