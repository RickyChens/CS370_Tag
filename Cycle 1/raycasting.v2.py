import pygame
import sys
import math
import pygame
from constants import *

# Initialize Pygame
pygame.init()

fov = 65  # FOV in degrees
halffov = fov / 2
ray_count = 550
ray_length = 125  # Max ray length
speed = 5
turn_speed = 0.1
transparent = (0, 0, 0, 0)
green = (0, 255, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycasting test")

# Starting position and direction
player_pos = [WIDTH // 2, HEIGHT // 2]
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
            pygame.quit()
            sys.exit()

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
        pygame.draw.line(screen, transparent, player_pos, ray_end)

    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    pygame.draw.circle(screen, WHITE, (int(player_pos[0]), int(player_pos[1])), 5)

    pygame.display.flip()
    screen.fill(green)
    pygame.time.Clock().tick(60)
