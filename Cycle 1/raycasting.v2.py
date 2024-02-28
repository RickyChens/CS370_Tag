import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
width, height = 800, 600
fov = 65  # FOV in degrees
halffov = fov / 2
ray_count = 550
ray_length = 125  # Max ray length
speed = 5
turn_speed = 10

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
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Player Movement
    dx, dy = 0, 0

    if keys[pygame.K_a]:
        dx -= speed
    if keys[pygame.K_d]:
        dx += speed
    if keys[pygame.K_w]:
        dy -= speed
    if keys[pygame.K_s]:
        dy += speed

    # Normalize diagonal movement
    if dx != 0 and dy != 0:
        dx /= math.sqrt(2)
        dy /= math.sqrt(2)

    player_pos[0] += dx
    player_pos[1] += dy

    # Vision Cone Movement
    if keys[pygame.K_LEFT]:
        player_angle -= turn_speed
    if keys[pygame.K_RIGHT]:
        player_angle += turn_speed

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
