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

    for i in range(ray_count):
        # Calculate the angle for the current ray
        angle = math.radians(start_angle + i * angle_increment)

        # Calculate the direction vector for the ray
        direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))

        # Initialize the ray endpoint
        ray_end = player_pos + direction * ray_length

        # Check for collisions with obstacles
        for obstacle in obstacles:
            # Check if the ray intersects with any part of the obstacle
            intersection = obstacle.rect.clipline(player_pos, ray_end)
            if intersection:
                # Adjust the ray endpoint to the intersection point
                ray_end = intersection[0]
        player_intersection = bot_rect.clipline(player_pos, ray_end)
        if player_intersection:
            collision_flag[0] = True

        # Draw the ray
        pygame.draw.line(screen, YELLOW_TRANSPARENT, player_pos, ray_end, 2)
