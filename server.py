#Basic server config
#Thomas Palackal



# server.py

import pygame
import socket
import json

# Server settings
SERVER_IP = '192.168.229.187'  # Localhost (change to your server IP if needed)
SERVER_PORT = 5555
BUFFER_SIZE = 1024

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print("Server started, waiting for connections...")

players = {}

def receive_data(client_socket):
    try:
        data = client_socket.recv(BUFFER_SIZE).decode()
        return json.loads(data)
    except:
        return None

def send_data_to_all(data):
    for client in players:
        client.send(json.dumps(data).encode())

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established.")

    player_id = addr[1]
    players[client_socket] = player_id

    while True:
        data = receive_data(client_socket)
        if not data:
            break

        # Update player positions or handle other game logic
        print(f"Received data from player {player_id}: {data}")

        # Broadcast the updated game state to all clients
        send_data_to_all(data)

    print(f"Player {player_id} disconnected")
    client_socket.close()
    del players[client_socket]
