import random
import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
screen_boundaries = pygame.Rect((0, 0), (HEIGHT, WIDTH))

mapping = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
           [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
           [1, 1, 1, 0, 1, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
           [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()

        self.image = pygame.Surface([50, 50])
        self.image.fill(color)
        self.image.set_colorkey((255, 100, 98))

        self.rect = self.image.get_rect(center=pos)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions with obstacles.
        if dx != 0 or dy != 0:
            self.move_single_axis(dx, dy)

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        for r in range(len(mapping)):
            for c in range(len(mapping[r])):
                if mapping[r][c] == 1:
                    obstacle_rect = pygame.Rect(c * (WIDTH // len(mapping[r])),
                                                r * (HEIGHT // len(mapping)),
                                                WIDTH // len(mapping[r]),
                                                HEIGHT // len(mapping))

                    if self.rect.colliderect(obstacle_rect):
                        if dx > 0:
                            self.rect.right = obstacle_rect.left
                        if dx < 0:
                            self.rect.left = obstacle_rect.right
                        if dy > 0:
                            self.rect.bottom = obstacle_rect.top
                        if dy < 0:
                            self.rect.top = obstacle_rect.bottom


player = Player((350, 350), WHITE)

obstacles = []
for r in range(len(mapping)):
    for c in range(len(mapping[r])):
        if mapping[r][c] == 1:
            obstacle = Player((c * (WIDTH // len(mapping[r])) + WIDTH // (2 * len(mapping[r])),
                               r * (HEIGHT // len(mapping)) + HEIGHT // (2 * len(mapping))),
                              RED)
            obstacles.append(obstacle)

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
    for r in range(len(mapping)):
        for c in range(len(mapping[r])):
            if mapping[r][c] == 1:
                rect_x = c * (WIDTH // len(mapping[r]))
                rect_y = r * (HEIGHT // len(mapping))
                rect_width = WIDTH // len(mapping[r])
                rect_height = HEIGHT // len(mapping)
                pygame.draw.rect(screen, RED, pygame.Rect(rect_x, rect_y, rect_width, rect_height), 2)

    for obstacle in obstacles:
        screen.blit(obstacle.image, obstacle.rect)

    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
