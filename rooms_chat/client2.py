import socket
import threading

def autentificate(client_socket):
    try:
        username = input("Zadejte své uživatelské jméno: ")
        password = input("Zadejte sve heslo: ")
        client_socket.send(f"{username}:{password}".encode('utf-8'))
        message = client_socket.recv(1024).decode('utf-8')
        print(message)
        return username

    except:
        print("Došlo k chybě!")
        client_socket.close()


def choose_room(client_socket):
    try:
        room = input("Zadejte room: ")
        client_socket.send(room.encode('utf-8'))
        return room

    except:
        print("Došlo k chybě!")
        client_socket.close()

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "CLOSE":
                client_socket.close()
            else:
                print(message)
        except:
            print("Došlo k chybě!")
            client_socket.close()
            break



def send_messages(client_socket, username):
    try:
        while True:
            message = f"{username}: {input('zadej spravu:')}"
            client_socket.send(message.encode('utf-8'))

    except:
        print("Došlo k chybě!")
        client_socket.close()

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    username = autentificate(client_socket)
    choose_room(client_socket)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket, username))
    send_thread.start()