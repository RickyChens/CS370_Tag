#Example client side networking config
#Thomas Palackal




# client.py
import pygame
import socket
import json

# Client settings
SERVER_IP = '192.168.229.187'  # The server's IP address
SERVER_PORT = 5555
BUFFER_SIZE = 1024

# Initialize Pygame and create window
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Multiplayer Tag Game")

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

def send_data(data):
    client_socket.send(json.dumps(data).encode())

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic (e.g., player movement) goes here
    # Example: send player position
    player_data = {'x': 100, 'y': 200}  # Replace with actual player position
    send_data(player_data)

    # Receive updates from the server
    try:
        server_data = json.loads(client_socket.recv(BUFFER_SIZE).decode())
        # Update game state based on server_data
    except:
        pass



    pygame.display.flip()

pygame.quit()
client_socket.close()
