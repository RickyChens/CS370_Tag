import pygame
import sys
import random
from constants import *
from button import Button
from Classes import Player, Obstacle, Modifier, Bot
from randomMap import generate_random_map
from Raycasting import raycast

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

    # Raycasting vars
    turn_left = False
    turn_right = False
    flashlight_angle = 0

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
    while True:
        x = random.randint(0, WIDTH - ball.rect.width)
        y = random.randint(0, HEIGHT - ball.rect.height)
        new_rect = pygame.Rect(x, y, ball.rect.width, ball.rect.height)

        # Check for collision with obstacles
        if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
            ball.rect.topleft = (x, y)
            break

        # Initialize the bot
    bot = Bot((100, 100))
    bot_group = pygame.sprite.Group()
    bot_group.add(bot)

    # Initialize the bot and ensure it doesn't collide with obstacles upon spawn
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
                elif event.key == pygame.K_LEFT:
                    turn_left = True
                elif event.key == pygame.K_RIGHT:
                    turn_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    turn_left = False
                elif event.key == pygame.K_RIGHT:
                    turn_right = False
            elif event.type == pygame.USEREVENT:
                player.resetSpeed()
                dx = 5
                dy = 5
            elif event.type == pygame.USEREVENT + 1:
                bot.resetSpeed()

        if turn_left:
            flashlight_angle -= 5  # Decrease flashlight angle
        if turn_right:
            flashlight_angle += 5  # Increase flashlight angle

        dx = 5 + player.speed_modifier
        dy = 5 + player.speed_modifier
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move(-dx, 0, obstacles, player_group)
        if keys[pygame.K_d]:
            player.move(dx, 0, obstacles, player_group)
        if keys[pygame.K_w]:
            player.move(0, -dy, obstacles, player_group)
        if keys[pygame.K_s]:
            player.move(0, dy, obstacles, player_group)

        bot_modifier = ball.checkCircleCollision(ball, bot_group, obstacles)
        if bot_modifier == 1:
            bot.speedBuff(5)
        elif bot_modifier == 0:
            bot.SlowDebuff(5)
        bot.move_towards_player(player.rect.topleft, obstacles, screen_boundaries)
        temp = ball.checkCircleCollision(ball, player_group, obstacles)
        if temp == 1:
            player.speedBuff(5)
        elif temp == 0:
            player.SlowDebuff(5)

        player.rect.clamp_ip(screen_boundaries)

        screen.blit(background, (0, 0))

        # Raycasting drawn and collision checked
        collision_flag = [False]
        raycast(screen, player.rect.center, flashlight_angle, obstacles, bot.rect, collision_flag)
        print(collision_flag[0])

        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)
        screen.blit(ball.image, ball.rect)
        if collision_flag[0]:
            screen.blit(bot.image, bot.rect)
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
