import pygame
import sys
from constants import *
from button import Button
from collision import Player, Obstacle
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_boundaries = pygame.Rect((0, 0), (WIDTH, HEIGHT))
background = pygame.image.load("Assets/Background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


def play():
    player = Player((500, 500))
    obstacle = Obstacle((300, 300), RED)

    player_group = pygame.sprite.Group()
    player_group.add(player)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.move(-5, 0, obstacle, player_group)
        if keys[pygame.K_RIGHT]:
            player.move(5, 0, obstacle, player_group)
        if keys[pygame.K_UP]:
            player.move(0, -5, obstacle, player_group)
        if keys[pygame.K_DOWN]:
            player.move(0, 5, obstacle, player_group)

        player.rect.clamp_ip(screen_boundaries)

        screen.fill(BLACK)
        screen.blit(player.image, player.rect)
        screen.blit(obstacle.image, obstacle.rect)
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
