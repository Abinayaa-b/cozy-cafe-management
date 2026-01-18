import sqlite3
conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("DELETE FROM menu")
menu_items = [
    ("Coffee", 50, "Yes"),
    ("Tea", 30, "Yes"),
    ("Sandwich", 80, "Yes"),
    ("Pasta", 120, "Yes"),
    ("Burger", 100, "Yes"),
]

cur.executemany(
    "INSERT INTO menu VALUES (NULL,?,?,?)",
    menu_items
)

conn.commit()
conn.close()
print("Menu updated successfully!")