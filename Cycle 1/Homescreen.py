import pygame
import sys
import random
from constants import *
from button import Button
from Classes import Player, Obstacle, Modifier
from randomMap import generate_random_map

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

    ball = Modifier((500, 500))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        dx = 5
        dy = 5
        if keys[pygame.K_LEFT]:
            player.move(-dx, 0, obstacles, player_group)
        if keys[pygame.K_RIGHT]:
            player.move(dx, 0, obstacles, player_group)
        if keys[pygame.K_UP]:
            player.move(0, -dy, obstacles, player_group)
        if keys[pygame.K_DOWN]:
            player.move(0, dy, obstacles, player_group)

        ball.checkCircleCollision(ball, player_group, obstacles)
        player.rect.clamp_ip(screen_boundaries)

        screen.blit(background, (0, 0))
        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)
        screen.blit(ball.image, ball.rect)
        screen.blit(player.image, player.rect)
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
