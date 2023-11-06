import socket
import selectors

sel = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()
    print("Server started. Waiting for connections...")
    sel.register(server_socket, selectors.EVENT_READ, accept_socket)


def accept_socket(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    sel.register(client_socket, selectors.EVENT_READ, conect_with_client)


def conect_with_client(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = 'Hello client\n'.encode()
        client_socket.send(response)
    else:
        sel.unregister(client_socket)
        client_socket.close()


def main_loop():
    while True:
        event = sel.select()
        for key, _ in event:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    main_loop()
