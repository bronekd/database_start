
import sqlite3


conn = sqlite3.connect("my_db_pracovni.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            city TEXT)""")

#cur.execute("""INSERT INTO users (name, age) VALUES ('Jan', 33)""")
cur.execute("""INSERT INTO users (name, age) VALUES (?, ?)""", ("Honza", 30))
cur.execute("""DELETE FROM users WHERE name='Honza'""")
#db_insert(cur, "users", ["name", "age"], ["Adam", 44])

conn.commit()

#cur.execute("SELECT * FROM users WHERE age='30'")
cur.execute("SELECT * FROM users")

rows = cur.fetchall()
print(rows)
print("-------")
for row in rows:
   print(row[1])
   print(row)

conn.close()
