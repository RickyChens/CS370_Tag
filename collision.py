import random
import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
screen_boundaries = pygame.Rect((0, 0), (HEIGHT, WIDTH))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()

        self.image = pygame.Surface([50, 50])
        self.image.fill(color)
        self.image.set_colorkey((255, 100, 98))

        self.rect = self.image.get_rect(center=pos)


player = Player((250, 250), WHITE)
obstacle = Player((random.randint(50, 750), random.randint(50, 750)), RED)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_LEFT]:
        dx = -10
    if keys[pygame.K_RIGHT]:
        dx = 10
    if keys[pygame.K_UP]:
        dy = -10
    if keys[pygame.K_DOWN]:
        dy = 10

    new_rect = player.rect.move(dx, dy)

    if not new_rect.colliderect(obstacle.rect):
        player.rect = new_rect
    else:
        nx = 0
        ny = 0
        if dx > 0:
            nx = 50 - (obstacle.rect.x - player.rect.x)
        elif dx < 0:
            nx = 50 - (player.rect.x - obstacle.rect.x)
        elif dy > 0:
            ny = 50 - (obstacle.rect.y - player.rect.y)
        elif dy < 0:
            ny = 50 - (player.rect.y - obstacle.rect.y)
        player.rect.x += nx
        player.rect.y += ny
        print("Collision")

    # Keeps player within window boundaries
    player.rect.clamp_ip(screen_boundaries)

    screen.fill(BLACK)
    screen.blit(player.image, player.rect)
    screen.blit(obstacle.image, obstacle.rect)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
