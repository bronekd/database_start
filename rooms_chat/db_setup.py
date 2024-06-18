import sqlite3


def setup_database():
    conn = sqlite3.connect('chat_server.db')
    cursor = conn.cursor()

    # Vytvorenie tabuľky pre používateľov
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Vytvorenie tabuľky pre miestnosti
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    # Vytvorenie tabuľky pre správy
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        room_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Pridanie testovacích používateľov
    users = [
        ('user1', 'pass1'),
        ('user2', 'pass2'),
        ('user3', 'pass3')
    ]
    cursor.executemany('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', users)

    # Pridanie testovacích miestností
    rooms = [
        ('General',),
        ('Technology',),
        ('Random',)
    ]
    cursor.executemany('INSERT OR IGNORE INTO rooms (name) VALUES (?)', rooms)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()