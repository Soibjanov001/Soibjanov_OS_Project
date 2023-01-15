import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 2334
ADDRESS = ('192.168.0.120', 2334)
SIZE = 1024
FORMAT = "utf-8"

connectedClients = []


def handle_client(connection, address):
    message = connection.recv(SIZE).decode(FORMAT)
    if message.split(' ')[1] in connectedClients:
        message = "ERROR! User Already Exists, Try Other Name!"
        connection.send(message.encode(FORMAT))
        connection.close()
    else:
        connectedClients.append(message.split(' ')[1])
        message = "OK! Connected to Server!"
        connection.send(message.encode(FORMAT))

        print(f"[NEW CONNECTION] {address} connected.")
        connected = True
        while connected:
            message = connection.recv(SIZE).decode(FORMAT)
            if message == 'disconnect':
                connected = False
                print(f"[{address}] {message}")
                message = f"OK! Disconnected from Server!"
                connection.send(message.encode(FORMAT))

            elif message == 'lu':
                message = f"List of Users: {connectedClients}"
                connection.send(message.encode(FORMAT))

            elif message == 'lf':
                filesList = os.listdir("FilesOnServer\\")
                message = f"List of Files on Server: {filesList}"
                connection.send(message.encode(FORMAT))

            elif 'read' == message.split(' ')[0] and len(message.split(' ')) == 2:
                fileName = message.split(' ')[1]
                if fileName in os.listdir("FilesOnServer\\"):
                    with open(f"FilesOnServer\\{fileName}", 'r') as file:
                        message = file.read()
                    fileSize = os.path.getsize(f"FilesOnServer\\{fileName}")
                    connection.send(f"File Size: {fileSize}\nFile Data: {message}".encode(FORMAT))
                else:
                    message = f"ERROR! File Not Found!"
                    connection.send(message.encode(FORMAT))

            elif 'write' == message.split(' ')[0] and len(message.split(' ')) == 2:
                fileName = message.split(' ')[1]
                if fileName in os.listdir("FilesOnServer\\"):
                    message = f"ERROR! File Already Exists!"
                    connection.send(message.encode(FORMAT))
                else:
                    message = f"OK!"
                    connection.send(message.encode(FORMAT))
                    message = connection.recv(SIZE).decode(FORMAT)
                    with open(f"FilesOnServer\\{fileName}", 'w') as file:
                        file.write(message)
                    message = f"OK! File Written!"
                    connection.send(message.encode(FORMAT))

        connection.close()


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
