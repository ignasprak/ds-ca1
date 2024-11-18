# Code used from other files:
# - The basic structure and socket handling were inspired by the echo server example from 1_13a_echo_server.py.
# - The threading and client handling logic were adapted from the marketplace_server.py file.
# - The notification mechanism to all clients was inspired by the marketplace_server.py file.

import socket
import threading
import time
import uuid

host = 'localhost'
port = 12345
items = {
    'flower': 5,
    'sugar': 5,
    'potato': 5,
    'oil': 5
}
current_item = None
item_lock = threading.Lock()
clients = []
client_ids = {}

def handle_client(client_socket, client_address):
    global current_item
    client_id = str(uuid.uuid4())
    client_ids[client_socket] = client_id
    client_socket.sendall("Welcome to the marketplace!".encode('utf-8'))  # Send welcome message to the client
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            if data.startswith('buy'):
                amount = int(data.split()[1])
                with item_lock:
                    if items[current_item] >= amount:
                        items[current_item] -= amount
                        client_socket.sendall(f"Purchase successful: {amount} of {current_item}".encode('utf-8'))
                        notify_all_clients(f"{client_ids[client_socket]} bought {amount} of {current_item}. Amount left: {items[current_item]}")
                    else:
                        client_socket.sendall(f"Not enough {current_item} left.".encode('utf-8'))
        except:
            break
    client_socket.close()
    del client_ids[client_socket]

def notify_all_clients(message):
    for client in clients:
        try:
            client.sendall(message.encode('utf-8'))
        except:
            clients.remove(client)

def start_server():
    global current_item
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"Connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

        if current_item is None:
            current_item = list(items.keys())[0]
            threading.Thread(target=sell_item).start()

def sell_item():
    global current_item
    while True:
        for i in range(60, 0, -1):
            notify_all_clients(f"Time left for selling {current_item}: {i} seconds")
            time.sleep(1)
        with item_lock:
            if items[current_item] > 0:
                continue
            else:
                current_item = list(items.keys())[(list(items.keys()).index(current_item) + 1) % len(items)]

if __name__ == "__main__":
    start_server()

