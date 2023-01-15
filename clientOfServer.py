import socket

# Client
IP = socket.gethostbyname(socket.gethostname())
PORT = 2334
ADDR = ('192.168.0.120', 2334)
SIZE = 9999
FORMAT = "utf-8"
DISCONNECT_message = "!DISCONNECT"


def main():
    command = input("Enter your command: ")

    if len(command.split(' ')) == 2 and 'connect' == command.split()[0]:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

        message = command
        client.send(message.encode(FORMAT))
        message = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {message}")

        if message == "OK! Connected to Server!":
            connected = True
            while connected:
                message = input("Enter your command: ")
                client.send(message.encode(FORMAT))
                if message == 'OK! Disconnected from Server!':
                    connected = False
                    print(f"[SERVER] {message}")
                else:
                    if 'write' == message.split(' ')[0] and len(message.split(' ')) == 2:
                        messageSub = client.recv(SIZE).decode(FORMAT)
                        if messageSub == "OK!":
                            with open(f"FilesOnClient\\{message.split(' ')[1]}", 'r') as file:
                                message = file.read()
                            client.send(message.encode(FORMAT))
                        else:
                            print(f"[SERVER] {messageSub}")
                            continue
                    message = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {message}")

    else:
        print("Invalid Command")


if __name__ == "__main__":
    main()
