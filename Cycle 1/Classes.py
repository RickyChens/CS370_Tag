import pygame
import random
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

class Bot(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        image = pygame.image.load("soldier.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, 0.25)
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 10
        self.move_cooldown = 0  # Cooldown period after each movement

    def move_towards_player(self, player_pos, obstacles, screen_boundaries):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return

        dx, dy = player_pos[0] - self.rect.x, player_pos[1] - self.rect.y
        directions = []
        if abs(dx) > abs(dy):
            directions.append(('right' if dx > 0 else 'left', self.speed, 0))
            directions.append(('down' if dy > 0 else 'up', 0, self.speed))
        else:
            directions.append(('down' if dy > 0 else 'up', 0, self.speed))
            directions.append(('right' if dx > 0 else 'left', self.speed, 0))

        # Avoid moving into corners
        if self.rect.left < 10:
            directions.append(('right', self.speed, 0))
        if self.rect.right > screen_boundaries.width - 10:
            directions.append(('left', -self.speed, 0))
        if self.rect.top < 10:
            directions.append(('down', 0, self.speed))
        if self.rect.bottom > screen_boundaries.height - 10:
            directions.append(('up', 0, -self.speed))

        # Add random direction to avoid getting stuck
        directions.append((random.choice(['left', 'right', 'up', 'down']), self.speed * random.choice([-1, 1]), self.speed * random.choice([-1, 1])))

        for direction, x_move, y_move in directions:
            new_rect = self.rect.move(x_move, y_move)
            if not any(new_rect.colliderect(obstacle) for obstacle in obstacles) and screen_boundaries.contains(new_rect):
                self.rect = new_rect
                self.move_cooldown = 10  # Set the cooldown period after moving
                break