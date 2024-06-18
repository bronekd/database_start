import socket
import threading
import sqlite3

rooms = {}

def broadcast(message, room, client_socket):
    """Odošle správu všetkým klientom v miestnosti okrem odosielateľa."""
    for client in rooms[room]:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                rooms[room].remove(client)
                if not rooms[room]:
                    del rooms[room]

def save_message(room_id, user_id, message):
    conn = sqlite3.connect('chat_server.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (room_id, user_id, message) VALUES (?, ?, ?)', (room_id, user_id, message))
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = sqlite3.connect('chat_server.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def get_room_id(room_name):
    conn = sqlite3.connect('chat_server.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM rooms WHERE name=?', (room_name,))
    room = cursor.fetchone()
    conn.close()
    return room[0] if room else None

def handle_client(client_socket, room, username):
    user_id = get_user_id(username)
    room_id = get_room_id(room)
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            save_message(room_id, user_id, message.decode('utf-8'))
            broadcast(message, room, client_socket)
        except:
            client_socket.close()
            rooms[room].remove(client_socket)
            if not rooms[room]:
                del rooms[room]
            break

def load_rooms():
    conn = sqlite3.connect('chat_server.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms')
    rooms_list = cursor.fetchall()
    conn.close()
    message = "Dostupné miestnosti:\n"
    for room in rooms_list:
        message += f"{room[0]}. {room[1]}\n"

    return message


def authenticate_user(username, password):
    conn = sqlite3.connect('chat_server.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def receive_connections(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Připojení od {client_address} bylo navázáno.")

        username, password = client_socket.recv(1024).decode('utf-8').split(":")

        if authenticate_user(username, password):
            client_socket.send("Připojení k serveru bylo úspěšné!".encode('utf-8'))

            print(f"Uživatelské jméno klienta je {username}")

            message = load_rooms()
            client_socket.send(message.encode())

            room = client_socket.recv(1024).decode('utf-8')
            if room not in rooms:
                rooms[room] = []
            rooms[room].append(client_socket)
            print(f"Klient sa pripojil do miestnosti: {room}")

            broadcast(f"{username} se připojil k chatu!".encode('utf-8'), room, client_socket)

            thread = threading.Thread(target=handle_client, args=(client_socket, room, username))
            thread.start()
        else:
            client_socket.send("Neplatné uživatelské jméno nebo heslo.".encode('utf-8'))
            client_socket.send("CLOSE".encode('utf-8'))
            client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen()

    print("Server naslouchá...")
    receive_connections(server_socket)

if __name__ == "__main__":
    start_server()