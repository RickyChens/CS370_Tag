import pygame
import sys
import random
from constants import *
from button import Button
from betaClasses import Player, Obstacle, Bot
from randomMap import generate_random_map

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("Assets/Background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def play():
    obstacles = []
    mapping = generate_random_map()
    for r in range(len(mapping)):
        for c in range(len(mapping[r])):
            if mapping[r][c] == 1:
                obstacle = Obstacle(r, c, mapping, WHITE)
                obstacles.append(obstacle)

    player = Player((500, 500))
    while True:
        x = random.randint(0, WIDTH - player.rect.width)
        y = random.randint(0, HEIGHT - player.rect.height)
        if not any(pygame.Rect(x, y, player.rect.width, player.rect.height).colliderect(obstacle.rect) for obstacle in obstacles):
            player.rect.topleft = (x, y)
            break
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bot = Bot((100, 100))
    bot.update_path(player.rect.topleft, mapping)

    bot_width = bot.rect.width
    bot_height = bot.rect.height
    while True:
        x = random.randint(0, WIDTH - bot_width)
        y = random.randint(0, HEIGHT - bot_height)
        new_rect = pygame.Rect(x, y, bot_width, bot_height)

        # Check for collision with obstacles
        if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
            bot.rect.topleft = (x, y)
            break

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

        player_moved = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-5, 0, obstacles, player_group)
            player_moved = True
        if keys[pygame.K_RIGHT]:
            player.move(5, 0, obstacles, player_group)
            player_moved = True
        if keys[pygame.K_UP]:
            player.move(0, -5, obstacles, player_group)
            player_moved = True
        if keys[pygame.K_DOWN]:
            player.move(0, 5, obstacles, player_group)
            player_moved = True

        if player_moved:
            bot.update_path(player.rect.topleft, mapping)

        bot.move_towards_player()

        screen.fill(BLACK)
        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)
        screen.blit(player.image, player.rect)
        screen.blit(bot.image, bot.rect)
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
