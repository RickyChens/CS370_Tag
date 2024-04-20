import pygame
import sys
import random
import socket
import pickle
import pygame_gui
from constants import *
from button import Button
from Classes import Player, Obstacle, Modifier, Bot, Background
from randomMap import generate_random_map
from Raycasting import raycast
from testing_sprite import getTile

# Initialize pygame window and necessary variables
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_boundaries = pygame.Rect((0, 0), (WIDTH, HEIGHT))
background = pygame.image.load("Assets/Background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
instructions = pygame.image.load("Assets/instructions.webp").convert_alpha()
player_sheet = pygame.image.load('Assets/Dungeon_Character.png').convert_alpha()
sprite_sheet = pygame.image.load('Assets/Dungeon_Tileset.png').convert_alpha()
red_sprite_sheet = pygame.image.load('Assets/Dungeon_Tileset.png').convert_alpha()
player_image = getTile(player_sheet, 16, 16, 2.5, BLACK, 80, 32)
bot_image = getTile(player_sheet, 16, 16, 2.5, BLACK, 80, 48)
light_tile = getTile(sprite_sheet, 16, 16, 10, BLACK, 32, 32)
obstacle_tile = getTile(sprite_sheet, 16, 16, 10, BLACK, 56, 80)
modifier_img = getTile(sprite_sheet, 16, 16, 2.5, BLACK, 96, 144-16)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Clock = pygame.time.Clock()
Manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Define a function to draw the gradient circle around the player
def draw_gradient_circle(screen, player_pos):
    gradient_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    max_radius = 50  # Maximum radius of the gradient circle
    for radius in range(max_radius, 0, -1):
        alpha = int(255 * (1 - radius / max_radius))  # Calculate alpha based on distance from max_radius
        pygame.draw.circle(gradient_surface, (0, 0, 0, alpha), player_pos, radius)
    screen.blit(gradient_surface, (0, 0))

# Define the play function
def play():
    # Asking for Map
    mapReq = pickle.dumps("map")
    s.send(mapReq)
    serialized_map = s.recv(1024)

    # Creating all random obstacles
    obstacles = []
    background_tiles = []
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

    initRadius = 100
    radius = (800 - initRadius) // 100
    circle_surface = pygame.Surface((radius * 23 * 2, radius * 23 * 2), pygame.SRCALPHA)
    for i in range(23):
        alpha = 255 / 100
        circle = pygame.Surface((radius * 23 * 2, radius * 23 * 2), pygame.SRCALPHA)
        circle_center = (radius * 23, radius * 23)
        pygame.draw.circle(circle, (0, 0, 0, int(alpha * i)), circle_center, radius * i, radius)
        circle_surface.blit(circle, (0, 0))

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
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

        coordinates = pickle.dumps((player.rect.x, player.rect.y))
        s.send(coordinates)

        coordReq = pickle.dumps("coord")
        s.send(coordReq)
        message = s.recv(1024)
        enemy_coordinates = pickle.loads(message)
        if enemy_coordinates == "waiting":
            print("Waiting")
        else:
            print(enemy_coordinates)
            bot.rect.topleft = enemy_coordinates

        # Bot Collision Detection with orb
        bot_modifier = ball.checkCircleCollision(ball, bot_group, obstacles)
        if bot_modifier == 1:
            bot.speedBuff(5)
        elif bot_modifier == 0:
            bot.SlowDebuff(5)

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

        # Draw the gradient circle around the player

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

        circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        circle_center = (player.rect.x + player.rect.width // 2, player.rect.y + player.rect.height // 2)
        pygame.draw.circle(circle, (0, 0, 0, 230), circle_center, 2000, 1848)
        screen.blit(circle_surface, (player.rect.x - 143, player.rect.y - 143))
        screen.blit(circle, (0, 0))

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
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if restart_button.checkInput(pygame.mouse.get_pos()):
                    play()
            if event.type == pygame.MOUSEBUTTONUP:
                if menu_button.checkInput(pygame.mouse.get_pos()):
                    menu()

def instructionsMenu():
    while True:
        screen.blit(instructions, (0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()


def connectionMenu():
    tag_menu = pygame.font.Font("Assets/GlitchGoblin.ttf", 100).render("Multiplayer", True, "#b68f40")
    menu_rect = tag_menu.get_rect(center=(390, 100))  # Center Text
    ip_text = pygame.font.Font("Assets/GlitchGoblin.ttf", 50).render("IP", True, "#b68f40")
    ip_rect = tag_menu.get_rect(center=(425, 300))  # Center Text
    port_text = pygame.font.Font("Assets/GlitchGoblin.ttf", 50).render("Port", True, "#b68f40")
    port_rect = tag_menu.get_rect(center=(350, 400))  # Center Text

    ip_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((195, 250), (500, 50)),
                                                   manager=Manager, object_id="#ip_text")
    port_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((195, 350), (500, 50)),
                                                     manager=Manager, object_id="#port_text")

    # Creation of Connect Button
    connect_button = Button(pygame.Surface([320, 80]), (390, 500), "Connect",
                            pygame.font.Font("Assets/GlitchGoblin.ttf", 65))

    ip = ""
    port = "1"

    error_font = pygame.font.Font(None, 36)  # Default font for error message
    error_text = ""  # Initialize error message as empty string
    while True:
        UI_REFRESH_RATE = Clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#ip_text":
                ip = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#port_text":
                port = event.text
            if event.type == pygame.MOUSEBUTTONUP:
                if connect_button.checkInput(pygame.mouse.get_pos()):
                    try:
                        s.connect((ip, int(port)))
                        play()
                    except (socket.error, TypeError, ConnectionError, ValueError) as e:
                        print(f"Error connecting: {e}")
                        print(f"IP: {ip}, Port: {port}")
                        error_text = "Invalid IP and/or Port"  # Set error message

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()

            Manager.process_events(event)

        Manager.update(UI_REFRESH_RATE)

        screen.blit(background, (0, 0))
        connect_button.draw(screen)
        Manager.draw_ui(screen)

        screen.blit(tag_menu, menu_rect)
        screen.blit(ip_text, ip_rect)
        screen.blit(port_text, port_rect)

        if error_text:
            error_surface = error_font.render(error_text, True, (255, 0, 0))
            error_rect = error_surface.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
            screen.blit(error_surface, error_rect)

        pygame.display.flip()

def menu():
    while True:
        # Background and Title Text
        screen.blit(background, (0, 0))
        tag_menu = pygame.font.Font("Assets/GlitchGoblin.ttf", 100).render("TAG", True, "#b68f40")
        menu_rect = tag_menu.get_rect(center=(390, 100))  # Center Text
        screen.blit(tag_menu, menu_rect)

        start_button = Button(pygame.Surface([230, 80]), (390, 300), "Start",
                              pygame.font.Font("Assets/GlitchGoblin.ttf", 65))
        quit_button = Button(pygame.Surface([230, 80]), (390, 600), "Quit",
                             pygame.font.Font("Assets/GlitchGoblin.ttf", 65))
        instructions_button = Button(pygame.Surface([460, 80]), (390, 400), "Instructions",
                                     pygame.font.Font("Assets/GlitchGoblin.ttf", 65))
        multiplayer_button = Button(pygame.Surface([460, 80]), (390, 500), "Multiplayer",
                                    pygame.font.Font("Assets/GlitchGoblin.ttf", 65))

        start_button.draw(screen)
        quit_button.draw(screen)
        instructions_button.draw(screen)
        multiplayer_button.draw(screen)
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
            if event.type == pygame.MOUSEBUTTONUP:
                if instructions_button.checkInput(pygame.mouse.get_pos()):
                    instructionsMenu()
            if event.type == pygame.MOUSEBUTTONUP:
                if multiplayer_button.checkInput(pygame.mouse.get_pos()):
                    connectionMenu()


menu()
