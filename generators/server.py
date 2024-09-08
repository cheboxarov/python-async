import socket
from select import select

# David Beazly
# 2015 PyCon
# Concurrency from the Ground up Live

tasks = []
clients = []

to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5000))

    server_socket.listen()

    while True:
        yield 'read', server_socket
        client_socket, addr = server_socket.accept()
        print("Got connection from", addr)
        tasks.append(client_loop(client_socket))


def client_loop(client_socket):
    global clients
    clients.append(client_socket)
    while True:
        yield "read", client_socket
        data = client_socket.recv(1024)
        if not data:
            break
        data = data.decode()
        print(data)
        yield "write", client_socket
        for client in clients:
            client.send(f"Message from client ({client_socket.getsockname()}) {data}\n".encode())
    client_socket.close()
    clients.remove(client_socket)
    print("Connection closed")


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
        try:
            task = tasks.pop(0)

            reason, sock = next(task)

            if reason == "read":
                to_read[sock] = task

            if reason == "write":
                to_write[sock] = task
        except StopIteration:
            pass


if __name__ == "__main__":
    tasks.append(server())
    event_loop()
