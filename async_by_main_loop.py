import socket
from select import select

event_list = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()

print("Server started. Waiting for connections...")


def accept_socket(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    event_list.append(client_socket)

def conect_with_client(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = 'Hello client\n'.encode()
        client_socket.send(response)
    else:
        client_socket.close()


def main_loop():
    while True:
        data, _, _ = select(event_list, [], [])
        for work_soc in data:
            if work_soc is server_socket:
                accept_socket(work_soc)
            else:
                conect_with_client(work_soc)


if __name__ == '__main__':
    event_list.append(server_socket)
    main_loop()