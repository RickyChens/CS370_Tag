import pygame
import sys
import random
from constants import *
from button import Button
from Classes import Player, Obstacle
from randomMap import generate_random_map


def raycast(screen, player_rect, obstacles, flashlight_angle):
    # Define flashlight parameters
    flashlight_length = 100

    # Calculate flashlight direction based on player's facing direction and flashlight angle
    facing_direction = pygame.math.Vector2(1, 0)  # Initial facing direction
    facing_direction.rotate_ip(flashlight_angle)

    # Calculate angle range for the flashlight cone
    half_angle = 30  # Half of the angle of the flashlight cone

    # Adjust opacity for rays
    ray_color = (255, 255, 0, 20)  # Yellow color with 100 alpha (transparency)

    # Cast rays within the flashlight cone
    for angle in range(int(-half_angle), int(half_angle) + 1):
        direction = facing_direction.rotate(angle)
        ray_end = player_rect.center + direction * flashlight_length

        # Draw ray with adjusted opacity
        pygame.draw.line(screen, ray_color, player_rect.center, ray_end, 2)

        # Check for obstacle collisions
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(ray_end):
                break

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

        raycast(screen, player.rect, obstacles, flashlight_angle)

        # Render only players and objects within the rays...

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
