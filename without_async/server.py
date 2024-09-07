import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))

server_socket.listen()

while True:
    client_socket, addr = server_socket.accept()
    print("Got connection from", addr)
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        data = data.decode()
        print(data)
        client_socket.send(data.encode())
    client_socket.close()
    print("Connection closed")
