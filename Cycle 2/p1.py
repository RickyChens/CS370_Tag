import time

import pygame
import sys
import random
import socket
import pickle
from constants import *
from button import Button
from Classes import Player, Obstacle, Modifier, Bot, Background
from Raycasting import raycast
from testing_sprite import getTile

# Initializing Window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_boundaries = pygame.Rect((0, 0), (WIDTH, HEIGHT))
background = pygame.image.load("Assets/Background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_sheet = pygame.image.load('Assets/Dungeon_Character.png').convert_alpha()
sprite_sheet = pygame.image.load('Assets/Dungeon_Tileset.png').convert_alpha()
red_sprite_sheet = pygame.image.load('Assets/Dungeon_Tileset.png').convert_alpha()
player_image = getTile(player_sheet, 16, 16, 2.5, BLACK, 80, 32)
bot_image = getTile(player_sheet, 16, 16, 2.5, BLACK, 80, 48)
light_tile = getTile(sprite_sheet, 16, 16, 10, BLACK, 32, 32)
# obstacle_tile = getTile(sprite_sheet, 16, 16, 10, BLACK, 56, 80)
obstacle_tile = getTile(sprite_sheet, 16, 16, 10, BLACK, 56, 80)
modifier_img = getTile(sprite_sheet, 16, 16, 2.5, BLACK, 96, 144-16)

""" 
Shitty looking graphics
sprite_sheet = pygame.image.load('Assets/RetroSpacePNG.png').convert_alpha()
red_sprite_sheet = pygame.image.load('Assets/RetroSpaceHell_PNG.png').convert_alpha()
player_image = getTile(player_sheet, 16, 16, 2.5, BLACK, 80, 32)
light_tile = getTile(sprite_sheet, 16, 16, 10, BLACK, 32, 32)
obstacle_tile = getTile(red_sprite_sheet, 16, 16, 10, BLACK, 32, 16)
"""

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
s.connect(('localhost', 5555))

def play():
    # Creating all random obstacles
    obstacles = []
    background_tiles = []

    # Send a 'get_map' request to the server
    s.sendall(b'get_map')

    # Receive the serialized map data from the server
    serialized_map = s.recv(1024)

    # Deserialize the map data
    mapping = pickle.loads(serialized_map)

    for r in range(len(mapping)):
        for c in range(len(mapping[r])):
            if mapping[r][c] == 1:
                obstacle = Obstacle(r, c, mapping, obstacle_tile)
                obstacles.append(obstacle)
            else:
                bg_tile = Background(r, c, mapping, light_tile)
                background_tiles.append(bg_tile)

    background_surface = pygame.Surface((WIDTH, HEIGHT))

    for bg in background_tiles:
        background_surface.blit(bg.image, bg.rect)

    # Raycasting vars
    turn_left = False
    turn_right = False
    flashlight_angle = 0

    # Initializing and randomizing player position
    player = Player((500, 500), player_image)
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

    ball = Modifier((500, 500), modifier_img)
    while True:
        x = random.randint(0, WIDTH - ball.rect.width)
        y = random.randint(0, HEIGHT - ball.rect.height)
        new_rect = pygame.Rect(x, y, ball.rect.width, ball.rect.height)

        # Check for collision with obstacles
        if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
            ball.rect.topleft = (x, y)
            break

        # Initialize the bot
    bot = Bot((100, 100), bot_image)
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

    # Random person starts tagged
    if random.randint(0, 10) % 2 == 1:
        player.setIsTagged(True)
    else:
        bot.setIsTagged(True)
    # Scorekeeping vars
    player_score = 0
    bot_score = 0
    tag_cooldown = 3
    tagged_time = 0
    time_tracker = 0

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    s.sendall(b'unready')  # Send 'unready' message to the server
                    ready_up_menu()
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

        # Bot Collision Detection with orb
        bot_modifier = ball.checkCircleCollision(ball, bot_group, obstacles)
        if bot_modifier == 1:
            bot.speedBuff(5)
        elif bot_modifier == 0:
            bot.SlowDebuff(5)
        bot.move_towards_player(player.rect.topleft, obstacles, screen_boundaries)

        # Player Collision Detection with orb
        player_modifier = ball.checkCircleCollision(ball, player_group, obstacles)
        if player_modifier == 1:
            player.speedBuff(5)
        elif player_modifier == 0:
            player.SlowDebuff(5)

        # Player bot collision detection
        if pygame.sprite.spritecollide(bot, player_group, False, pygame.sprite.collide_mask):
            print("Collided")
            if player.getIsTagged() and tag_cooldown <= 0:
                tagged_time = 0
                tag_cooldown = 3
                bot.setIsTagged(True)
                player.setIsTagged(False)
            elif bot.getIsTagged() and tag_cooldown <= 0:
                tagged_time = 0
                tag_cooldown = 3
                player.setIsTagged(True)
                bot.setIsTagged(False)

        time_tracker += 1
        if time_tracker % 60 == 1:
            tag_cooldown -= 1

        if player.getIsTagged():
            tagged_time += 1
            if tagged_time % (5 * 60) == 0:
                bot_score += 1
        else:
            tagged_time += 1
            if tagged_time % (5 * 60) == 0:
                player_score += 1

        player.rect.clamp_ip(screen_boundaries)

        # Draw background
        screen.blit(background_surface, (0, 0))

        # Raycasting drawn and collision checked
        collision_flag = [False]
        raycast(screen, player.rect.center, flashlight_angle, obstacles, bot.rect, collision_flag)
        # print(collision_flag[0])

        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)

        screen.blit(ball.image, ball.rect)
        if collision_flag[0]:
            screen.blit(bot.image, bot.rect)
        screen.blit(player.image, player.rect)

        font = pygame.font.Font(None, 36)
        player_score_text = font.render(f'Player Score: {player_score}', True, RED)
        bot_score_text = font.render(f'Bot Score: {bot_score}', True, RED)
        if player.getIsTagged():
            tagged_text = font.render(f"Player is Tagged!", True, RED)
        else:
            tagged_text = font.render(f"Bot is Tagged!", True, RED)
        screen.blit(tagged_text, (10, 50))
        screen.blit(player_score_text, (10, 10))
        screen.blit(bot_score_text, (WIDTH - 150, 10))

        # Game ending
        if time_tracker / 60 >= 120: # If the time is more than 120 seconds
            if player_score > bot_score:
                winnerMenu("player")
            elif bot_score > player_score:
                winnerMenu("bot")
            elif bot_score == player_score:
                winnerMenu("tie")
        pygame.display.flip()
        clock.tick(60)

def ready_up_menu():
    while True:
        screen.blit(background, (0, 0))
        ready_up_text = pygame.font.Font("Assets/GlitchGoblin.ttf", 50).render("Ready Up", True, "#b68f40")
        ready_up_rect = ready_up_text.get_rect(center=(390, 150))
        screen.blit(ready_up_text, ready_up_rect)
        try:
            s.sendall(b'get_clients')
        except (BrokenPipeError, ConnectionResetError):
            print("Server disconnected")
            menu()

        # Receive the current number of clients from the server
        current_clients = pickle.loads(s.recv(1024))

        print(current_clients)

        ready_button = Button(pygame.Surface([230, 80]), (390, 300), "Ready",
                              pygame.font.Font("Assets/GlitchGoblin.ttf", 65))
        unready_button = Button(pygame.Surface([230, 80]), (390, 400), "Unready",
                                pygame.font.Font("Assets/GlitchGoblin.ttf", 65))  # New Unready button
        back_button = Button(pygame.Surface([230, 80]), (390, 500), "Back",
                             pygame.font.Font("Assets/GlitchGoblin.ttf", 65))

        if ready_button.pressed:
            pygame.draw.rect(screen, (0, 255, 0), ready_button.rect)  # Draw a green rectangle
        ready_button.draw(screen)
        unready_button.draw(screen)  # Draw the Unready button
        back_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
            if event.type == pygame.MOUSEBUTTONUP:
                if ready_button.checkInput(pygame.mouse.get_pos()):
                    if ready_button.pressed:
                        s.sendall(b'ready')
                if unready_button.checkInput(pygame.mouse.get_pos()):  # If Unready button is clicked
                    s.sendall(b'unready')  # Send 'unready' message to the server
                if back_button.checkInput(pygame.mouse.get_pos()):
                    menu()


        s.sendall(b'get_start')
        print("Test")
        status = s.recv(1024)
        print(status)
        if status == b'start':
            play()

def winnerMenu(winner):
    while True:
        screen.blit(background, (0, 0))
        if winner == "player":
            winner_text = (pygame.font.Font("Assets/GlitchGoblin.ttf", 50).
                           render("Player is the Winner!", True, "#b68f40"))
        elif winner == "bot":
            winner_text = (pygame.font.Font("Assets/GlitchGoblin.ttf", 50).
                           render("Bot is the Winner!", True, "#b68f40"))
        elif winner == "tie":
            winner_text = (pygame.font.Font("Assets/GlitchGoblin.ttf", 50).
                           render("It's a TIE!", True, "#b68f40"))
        winner_rect = winner_text.get_rect(center=(390, 150))
        screen.blit(winner_text, winner_rect)

        restart_button = Button(pygame.Surface([230, 80]), (390, 300), "Retry",
                                pygame.font.Font("Assets/GlitchGoblin.ttf", 65))
        menu_button = Button(pygame.Surface([230, 80]), (390, 400), "Menu",
                             pygame.font.Font("Assets/GlitchGoblin.ttf", 65))

        restart_button.draw(screen)
        menu_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if restart_button.checkInput(pygame.mouse.get_pos()):
                    play()
            if event.type == pygame.MOUSEBUTTONUP:
                if menu_button.checkInput(pygame.mouse.get_pos()):
                    menu()


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
                s.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if quit_button.checkInput(pygame.mouse.get_pos()):
                    s.close()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.checkInput(pygame.mouse.get_pos()):
                    ready_up_menu()



menu()
