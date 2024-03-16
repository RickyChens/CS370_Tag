import pygame
from constants import *
from button import Button
import pygame_gui
import sys

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_boundaries = pygame.Rect((0, 0), (WIDTH, HEIGHT))
background = pygame.image.load("Assets/Background.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

Clock = pygame.time.Clock()
Manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Creation of text input on screen
ip_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 275), (600, 50)),
                                               manager=Manager, object_id="#ip_text")
port_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((100, 375), (600, 50)),
                                                 manager=Manager, object_id="#port_text")

# Creation of Connect Button
connect_button = Button(pygame.Surface([320, 80]), (390, 500), "Connect",
                        pygame.font.Font("Assets/GlitchGoblin.ttf", 65))


def text_input():
    ip = -1
    port = -1
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
                    print("ip = " + str(ip) + "\t port = " + str(port))
            Manager.process_events(event)

        Manager.update(UI_REFRESH_RATE)

        screen.blit(background, (0, 0))
        connect_button.draw(screen)
        Manager.draw_ui(screen)

        pygame.display.flip()


text_input()
