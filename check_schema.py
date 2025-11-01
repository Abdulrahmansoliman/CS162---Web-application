import sqlite3

conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()

print("=" * 80)
print("TABLE SCHEMA")
print("=" * 80)
cursor.execute("PRAGMA table_info(todo_items)")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n" + "=" * 80)
print("SAMPLE DATA - First 15 items")
print("=" * 80)
cursor.execute('SELECT id, title, parent_id FROM todo_items LIMIT 15')
for row in cursor.fetchall():
    print(f"  ID: {row[0]:2d}, Parent: {str(row[2]):4s}, Title: {row[1]}")

conn.close()
