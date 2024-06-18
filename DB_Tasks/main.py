import sqlite3


conn = sqlite3.connect("chat_app.db")

cur = conn.cursor()


# Task1
# Ziskajte všechny spravy a jmena jejich autoru z db

cur.execute("""
SELECT messages.message, users.username
FROM messages
INNER JOIN users ON messages.user_id = users.id;
""")
print("Task1")
data = cur.fetchall()
print(data)


# Task2
# Ziskejte seznam všech mistnosti a poslednich 5 sprav z nich
cur.execute("""
SELECT rooms.name, messages.message
FROM rooms
LEFT JOIN messages ON rooms.id = messages.room_id
ORDER BY messages.id DESC;
""")
print("Task2")
data = cur.fetchall()
print(data)

# Task3
# Ziskejte vŠechny spravy za poslednich 24 hodin a jmena jejich autorov
cur.execute("""
SELECT messages.message, users.username
FROM messages
LEFT JOIN users ON messages.user_id = users.id
WHERE messages.timestamp >= datetime('now', '-1 day');
""")
print("Task3")
data = cur.fetchall()
print(data)

# Task 4
# ziskejte zoznam použivatelov a poČet sprav ktere kazdy napsal

cur.execute("""
SELECT users.username, COUNT(messages.id) AS mesage_count
FROM users
LEFT JOIN messages on users.id = messages.user_id
GROUP BY users.id;
""")
print("Task4")
data = cur.fetchall()
print(data)

# Task 5
# ziskejte zoznam mistnosti a pocet sprav v kazydej z nich


# Task 6
# ziskajte zoznam pouzivatelov a ich celkovy pocet prispevkov v jednotlivych miestnostiach


conn.close()