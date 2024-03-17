import math

import pygame
import random
from constants import *


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        image = pygame.image.load("soldier.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, 0.25)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.speed_modifier = 0
        self.isTagged = False

    def getIsTagged(self):
        return self.isTagged

    def setIsTagged(self, flag):
        self.isTagged = flag

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

    def speedBuff(self, duration):
        self.speed_modifier = 2
        pygame.time.set_timer(pygame.USEREVENT, duration * 1000)  # Set a timer to reset the speed after duration

    def SlowDebuff(self, duration):
        self.speed_modifier = -2
        pygame.time.set_timer(pygame.USEREVENT, duration * 1000)  # Set a timer to reset the speed after duration

    def resetSpeed(self):
        self.speed_modifier = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, r, c, mapping, color):
        super().__init__()
        # pygame.Rect(c * (WIDTH // len(mapping[r])),
        #             r * (HEIGHT // len(mapping)),
        #             WIDTH // len(mapping[r]),
        #             HEIGHT // len(mapping))

        image = pygame.image.load("Assets/gendtiles.webp").convert_alpha()
        self.image = pygame.transform.scale(image, (WIDTH // len(mapping[r]) + 1,
                                                    HEIGHT // len(mapping) + 1))
        # self.image = pygame.Surface([WIDTH // len(mapping[r]) + 1,
        #                              HEIGHT // len(mapping) + 1])
        pos = (c * (WIDTH // len(mapping[r])), r * (HEIGHT // len(mapping)))
        self.rect = self.image.get_rect(topleft=pos)


class Background(pygame.sprite.Sprite):
    def __init__(self, r, c, mapping, image):
        super().__init__()

        self.image = image
        self.image = pygame.transform.scale(image, (WIDTH // len(mapping[r]) + 1,
                                                    HEIGHT // len(mapping) + 1))
        pos = (c * (WIDTH // len(mapping[r])), r * (HEIGHT // len(mapping)))
        self.rect = self.image.get_rect(topleft=pos)


class Modifier(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        image = pygame.image.load("Assets/black dot.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, 0.025)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)

    def checkCircleCollision(self, modifier, player_group, obstacles):
        if pygame.sprite.spritecollide(modifier, player_group, False, pygame.sprite.collide_mask):
            while True:
                x = random.randint(0, WIDTH - self.rect.width)
                y = random.randint(0, HEIGHT - self.rect.height)
                new_rect = pygame.Rect(x, y, self.rect.width, self.rect.height)

                # Check for collision with obstacles
                if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
                    self.rect.topleft = (x, y)
                    break
            if random.random() < 0.33:
                print("Speed")
                return 1
            else:
                print("Slow")
                return 0


class Bot(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        image = pygame.image.load("soldier.png").convert_alpha()
        self.image = pygame.transform.scale_by(image, 0.25)
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 10
        self.move_cooldown = 0  # Cooldown period after each movement
        self.speed_modifier = 0
        self.isTagged = False

    def getIsTagged(self):
        return self.isTagged

    def setIsTagged(self, flag):
        self.isTagged = flag

    def move_towards_player(self, player_pos, obstacles, screen_boundaries):
        self.speed = 10 + self.speed_modifier
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        # print(self.speed)
        dx, dy = player_pos[0] - self.rect.x, player_pos[1] - self.rect.y
        directions = [
            ('right', self.speed, 0),
            ('left', -self.speed, 0),
            ('down', 0, self.speed),
            ('up', 0, -self.speed),
            ('downright', self.speed, self.speed),
            ('downleft', -self.speed, self.speed),
            ('upright', self.speed, -self.speed),
            ('upleft', -self.speed, -self.speed)
        ]

        # Find the direction that minimizes the distance to the player
        min_distance = float('inf')
        best_direction = None
        for direction, x_move, y_move in directions:
            new_rect = self.rect.move(x_move, y_move)
            if not any(new_rect.colliderect(obstacle) for obstacle in obstacles) and screen_boundaries.contains(
                    new_rect):
                new_distance = distance((new_rect.x, new_rect.y), player_pos)
                if new_distance < min_distance:
                    min_distance = new_distance
                    best_direction = (x_move, y_move)

        # Move in the best direction
        if best_direction:
            self.rect.move_ip(*best_direction)
            self.move_cooldown = 10  # Set the cooldown period after moving

    def speedBuff(self, duration):
        self.speed_modifier = 4
        pygame.time.set_timer(pygame.USEREVENT + 1, duration * 1000)  # Set a timer to reset the speed after duration

    def SlowDebuff(self, duration):
        self.speed_modifier = -4
        pygame.time.set_timer(pygame.USEREVENT + 1, duration * 1000)  # Set a timer to reset the speed after duration

    def resetSpeed(self):
        self.speed_modifier = 0
