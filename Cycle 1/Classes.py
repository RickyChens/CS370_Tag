import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        image = pygame.image.load("soldier.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, 0.25)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)

    def move(self, dx, dy, obstacles, player_group):
        if dx != 0 or dy != 0:
            self.move_single_axis(dx, dy, obstacles, player_group)

    def move_single_axis(self, dx, dy, obstacles, player_group):
        steps_x = abs(dx) + 1
        steps_y = abs(dy) + 1

        for i in range(max(steps_x, steps_y)):
            old_rect = self.rect.copy()
            self.rect.x += dx / steps_x
            self.rect.y += dy / steps_y
            for obstacle in obstacles:
                if pygame.sprite.spritecollide(obstacle, player_group, False, pygame.sprite.collide_mask):
                    self.rect = old_rect
                    break


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, r, c, mapping, color):
        super().__init__()
        # pygame.Rect(c * (WIDTH // len(mapping[r])),
        #             r * (HEIGHT // len(mapping)),
        #             WIDTH // len(mapping[r]),
        #             HEIGHT // len(mapping))

        self.image = pygame.Surface([WIDTH // len(mapping[r]),
                                     HEIGHT // len(mapping)])
        self.image.fill(color)
        self.image.set_colorkey((255, 100, 98))
        pos = (c * (WIDTH // len(mapping[r])), r * (HEIGHT // len(mapping)))
        self.rect = self.image.get_rect(topleft=pos)