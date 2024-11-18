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
countdown_thread = None
# Define a global stop event
stop_event = threading.Event()

def handle_client(client_socket, client_address):
    """
    Handle communication with a connected client.
    """
    global current_item, countdown_thread, stop_event
    client_id = str(uuid.uuid4())
    client_ids[client_socket] = client_id
    client_socket.sendall("\nWelcome to the marketplace!".encode('utf-8'))  # Send welcome message to the client
    notify_all_clients(f"\nClient {client_id} connected. Total clients: {len(clients)}")
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
                        client_socket.sendall(f"\nPurchase successful: {amount} of {current_item}\n".encode('utf-8'))
                        notify_all_clients(f"\n{client_ids[client_socket]} bought {amount} of {current_item}. \nAmount left: {items[current_item]}")
                        print(f"\nAmount left of {current_item}: {items[current_item]}")
                        if items[current_item] == 0:
                            notify_all_clients(f"\nStock sold out! Now selling: {current_item}")
                            current_item = list(items.keys())[(list(items.keys()).index(current_item) + 1) % len(items)]
                            stop_event.set()  # Signal the current countdown thread to stop
                            stop_event = threading.Event()  # Create a new event for the new countdown thread
                            countdown_thread = threading.Thread(target=sell_item, args=(stop_event,))
                            countdown_thread.start()  # Start the new countdown thread
                    else:
                        client_socket.sendall(f"\nNot enough {current_item} left.".encode('utf-8'))
        except:
            break
    client_socket.close()
    del client_ids[client_socket]
    clients.remove(client_socket)
    notify_all_clients(f"\nClient {client_id} disconnected. Total clients: {len(clients)}")

def notify_all_clients(message):
    """
    Send a message to all connected clients.
    """
    for client in clients:
        try:
            client.sendall(message.encode('utf-8'))
        except:
            clients.remove(client)

def start_server():
    """
    Start the server and accept client connections.
    """
    global current_item
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    current_item = list(items.keys())[0]
    threading.Thread(target=sell_item, args=(stop_event,)).start()

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"\r{' ' * 50}\rConnection from {client_address}. Total clients: {len(clients)}")  # Clear the last countdown and print connection message
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

def sell_item(stop_event):
    """
    Manage the selling of items, switching items every 60 seconds or when sold out.
    """
    global current_item
    for i in range(60, 0, -1):
        if stop_event.is_set():
            return  # Exit the function if the stop event is set
        with item_lock:
            print(f"\rTime left for selling {current_item}: {i} seconds", end='')
        time.sleep(1)
    print()  # Move to the next line after countdown
    with item_lock:
        print(f"Amount left of {current_item}: {items[current_item]}")
        current_item = list(items.keys())[(list(items.keys()).index(current_item) + 1) % len(items)]
        print(f"Now selling: {current_item}")
        # Reset the timer for the next product
        stop_event = threading.Event()  # Create a new event for the new countdown thread
        countdown_thread = threading.Thread(target=sell_item, args=(stop_event,))
        countdown_thread.start()

if __name__ == "__main__":
    stop_event = threading.Event()
    start_server()

