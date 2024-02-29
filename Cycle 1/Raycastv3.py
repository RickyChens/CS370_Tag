import pygame
import sys
import random
import math
from constants import *
from button import Button
from Classes import Player, Obstacle
from randomMap import generate_random_map

YELLOW_TRANSPARENT = (255, 255, 0, 100)  # Yellow color with alpha value 100 for transparency

def raycast(screen, player_pos, player_angle, obstacles):
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

        # Draw the ray
        pygame.draw.line(screen, YELLOW_TRANSPARENT, player_pos, ray_end, 2)


# Initializing Window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_boundaries = pygame.Rect((0, 0), (WIDTH, HEIGHT))
background = pygame.image.load("Assets/Background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


def play():
    # Creating all random obstacles
    obstacles = []
    mapping = generate_random_map()
    for r in range(len(mapping)):
        for c in range(len(mapping[r])):
            if mapping[r][c] == 1:
                obstacle = Obstacle(r, c, mapping, WHITE)
                obstacles.append(obstacle)

    # Initializing and randomizing player position
    player = Player((500, 500))
    player_width = player.rect.width
    player_height = player.rect.height
    while True:
        x = random.randint(0, WIDTH - player_width)
        y = random.randint(0, HEIGHT - player_height)
        new_rect = pygame.Rect(x, y, player_width, player_height)

        # Check for collision with obstacles
        if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
            player.rect.topleft = (x, y)
            break
    player_group = pygame.sprite.Group()
    player_group.add(player)

    clock = pygame.time.Clock()

    running = True

    turn_left = False
    turn_right = False
    flashlight_angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    turn_left = True
                elif event.key == pygame.K_RIGHT:
                    turn_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    turn_left = False
                elif event.key == pygame.K_RIGHT:
                    turn_right = False

        if turn_left:
            flashlight_angle -= 5  # Decrease flashlight angle
        if turn_right:
            flashlight_angle += 5  # Increase flashlight angle

        keys = pygame.key.get_pressed()

        # Movement based on WASD keys
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -5
        if keys[pygame.K_d]:
            dx = 5
        if keys[pygame.K_w]:
            dy = -5
        if keys[pygame.K_s]:
            dy = 5
        player.move(dx, dy, obstacles, player_group)

        player.rect.clamp_ip(screen_boundaries)

        screen.fill(BLACK)

        raycast(screen, player.rect.center, flashlight_angle, obstacles)  # Call raycasting function

        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)

        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def menu():
    while True:
        # Background and Title Text
        screen.blit(background, (0, 0))
        tag_menu = pygame.font.Font("Assets/GlitchGoblin.ttf", 100).render("TAG", True, "#b68f40")
        menu_rect = tag_menu.get_rect(center=(390, 150))  # Center Text
        screen.blit(tag_menu, menu_rect)

        start_button = Button(pygame.Surface([230, 80]), (390, 300), "Start",
                              pygame.font.Font("Assets/GlitchGoblin.ttf", 65))
        quit_button = Button(pygame.Surface([230, 80]), (390, 400), "Quit",
                             pygame.font.Font("Assets/GlitchGoblin.ttf", 65))

        start_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if quit_button.checkInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.checkInput(pygame.mouse.get_pos()):
                    play()


menu()