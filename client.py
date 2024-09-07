import socket

host = "localhost"
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    print(f"Подключено к серверу {host}:{port}")
    while True:
        message = input()
        client_socket.sendall(message.encode())

        response = client_socket.recv(1024)
        print(f"Ответ от сервера: {response.decode()}")
finally:
    client_socket.close()
