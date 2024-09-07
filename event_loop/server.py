import socket
from select import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))

server_socket.listen()

to_monitor = []


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")
    to_monitor.append(client_socket)


def send_message(client_socket):
    message = client_socket.recv(1024)
    if not message:
        client_socket.close()
        return
    response = message.decode()
    print(f"Message from client: {response}")
    client_socket.send(response.encode())


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])

        for socket in ready_to_read:
            if socket is server_socket:
                accept_connection(socket)
                continue
            send_message(socket)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
