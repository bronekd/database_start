# vzor od učitele
import sqlite3


conn = sqlite3.connect("my_db.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER)""")

cur.execute("""INSERT INTO users (name, age) VALUES ('Jan', 33)""")
cur.execute("""INSERT INTO users (name, age) VALUES (?, ?)""", ("Adam", 23))

#db_insert(cur, "users", ["name", "age"], ["Adam", 44])

conn.commit()

cur.execute("SELECT * FROM users")
rows = cur.fetchall()
print(rows)
print("-------")
for row in rows:
   print(row[1])

conn.close()
