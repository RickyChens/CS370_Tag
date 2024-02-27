import pygame
import sys
import math
import socket
import pickle

# Set up a socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)  # Change
client_socket.connect(server_address)

def send_player_data(position):
    serialized_data = pickle.dumps({'position': position})
    client_socket.sendall(serialized_data)

    # Receive a response from the server
    response = client_socket.recv(1024)
    print("Server response:", pickle.loads(response))


# Initialize Pygame
pygame.init()

# Constants
width, height = 800, 600
fov = 65  # FOV in degrees
halffov = fov / 2
ray_count = 550
ray_length = 125  # Max ray length
speed = 5
turn_speed = 0.1

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Raycasting test")

# Starting position and direction
player_pos = [width // 2, height // 2]
player_angle = 0

# Obstacles
obstacles = [
    pygame.Rect(200, 200, 50, 200),
    pygame.Rect(400, 100, 200, 50),
    pygame.Rect(600, 300, 50, 200)
]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client_socket.close()
            pygame.quit()
            sys.exit()

    send_player_data(player_pos)

    mouse_pos = pygame.mouse.get_pos()
    angle_to_mouse = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
    player_angle = math.degrees(angle_to_mouse)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= turn_speed
    if keys[pygame.K_RIGHT]:
        player_angle += turn_speed
    if keys[pygame.K_UP]:
        dx = speed * math.cos(math.radians(player_angle))
        dy = speed * math.sin(math.radians(player_angle))
        player_pos[0] += dx
        player_pos[1] += dy
    if keys[pygame.K_DOWN]:
        dx = -speed * math.cos(math.radians(player_angle))
        dy = -speed * math.sin(math.radians(player_angle))
        player_pos[0] += dx
        player_pos[1] += dy

    # Raycasting
    for ray in range(ray_count):
        ray_angle = (player_angle - halffov) + (ray / ray_count) * fov
        ray_direction = [math.cos(math.radians(ray_angle)), math.sin(math.radians(ray_angle))]

        end_point = [player_pos[0] + ray_direction[0] * ray_length, player_pos[1] + ray_direction[1] * ray_length]
        ray_end = end_point
        for obstacle in obstacles:
            intersection = obstacle.clipline(player_pos, end_point)
            if intersection:
                ray_end = intersection[0]
                break
        pygame.draw.line(screen, white, player_pos, ray_end)

    for obstacle in obstacles:
        pygame.draw.rect(screen, red, obstacle)

    pygame.draw.circle(screen, white, (int(player_pos[0]), int(player_pos[1])), 5)

    pygame.display.flip()
    screen.fill(black)
    pygame.time.Clock().tick(60)
