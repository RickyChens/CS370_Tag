import random
import pygame
import time
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

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.colliderect(obstacle.rect):
            if dx > 0:
                self.rect.right = obstacle.rect.left
            if dx < 0:
                self.rect.left = obstacle.rect.right
            if dy > 0:
                self.rect.bottom = obstacle.rect.top
            if dy < 0:
                self.rect.top = obstacle.rect.bottom


player = Player((250, 250), WHITE)
obstacle = Player((random.randint(50, 750), random.randint(50, 750)), RED)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.move(-2, 0)
    if keys[pygame.K_RIGHT]:
        player.move(2, 0)
    if keys[pygame.K_UP]:
        player.move(0, -2)
    if keys[pygame.K_DOWN]:
        player.move(0, 2)

    # Keeps player within window boundaries
    player.rect.clamp_ip(screen_boundaries)

    screen.fill(BLACK)
    screen.blit(player.image, player.rect)
    screen.blit(obstacle.image, obstacle.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
