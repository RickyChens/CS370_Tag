import pygame
import math
from constants import *

def raycast(screen, player_pos, player_angle, obstacles, bot_rect, collision_flag):
    # Constants for raycasting
    fov = 60  # Field of view in degrees
    ray_count = 150  # Number of rays
    ray_length = 150  # Max ray length

    # Calculate the starting angle for the cone
    start_angle = player_angle - fov / 2

    # Calculate the angle increment for each ray
    angle_increment = fov / ray_count

    # List to store endpoints of all rays
    ray_endpoints = []

    for i in range(ray_count):
        # Calculate the angle for the current ray
        angle = math.radians(start_angle + i * angle_increment)

        # Calculate the direction vector for the ray
        direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))

        # Initialize the ray start and end points
        ray_start = player_pos
        ray_end = player_pos + direction * ray_length

        # Flag to track if the ray hit an obstacle
        ray_hit_obstacle = False

        # Iterate through obstacles to check for collisions
        for obstacle in obstacles:
            # Check if the ray intersects with any part of the obstacle
            intersection = obstacle.rect.clipline(ray_start, ray_end)
            if intersection:
                # Adjust the ray endpoint to the intersection point
                ray_end = intersection[0]
                ray_hit_obstacle = True
                break  # No need to check further obstacles

        # Check for collision with the bot rectangle
        if not ray_hit_obstacle:
            player_intersection = bot_rect.clipline(ray_start, ray_end)
            if player_intersection:
                collision_flag[0] = True

        # Store the endpoint of the ray
        ray_endpoints.append(ray_end)

        # Draw the ray
        pygame.draw.line(screen, MILKY_WHITE_TRANSPARENT, ray_start, ray_end, 3)

    # Load the image
    image = pygame.image.load("Assets/lightfile.png").convert_alpha()  # Replace "path/to/image.png" with the actual path
    image.set_colorkey(BLACK)
    # Blit the image onto the screen