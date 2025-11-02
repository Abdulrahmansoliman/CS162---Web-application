"""
Migration script to add priority column to todo_items table
"""

from app import create_app
from models import db

app = create_app()

with app.app_context():
    try:
        # Add priority column with default value
        with db.engine.connect() as conn:
            conn.execute(db.text("""
                ALTER TABLE todo_items 
                ADD COLUMN priority VARCHAR(20) DEFAULT 'medium' NOT NULL
            """))
            conn.commit()
        print("✅ Successfully added priority column to todo_items table")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Column may already exist or there's a database issue")
