# Code used from other files:
# - The basic structure and socket handling were inspired by the echo client example from 1_13b_echo_client.py.
# - The threading and message receiving logic were adapted from the marketplace_client.py file.
# - The command input and sending mechanism were inspired by the marketplace_client.py file.

import socket
import sys
import threading

host = 'localhost'
port = 12345

def receive_messages(client_socket):
    """
    Continuously receive messages from the server.
    """
    while True:
        try:
            response = client_socket.recv(1024).decode('utf-8')
            if response:
                print(response)
        except:
            break

def main():
    """
    Main function to connect to the server and handle user commands.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(client_socket,)).start() # Creates a new thread and allows it run concurrently with recieve_messages function, and specifies the function to be execueted ion the new thread

    while True:
        command = input("Enter command (buy <amount>, list, exit): ")
        if command == 'exit':
            break
        client_socket.sendall(command.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()

