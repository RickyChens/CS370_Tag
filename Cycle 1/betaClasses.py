import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
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
        self.path = []
        self.move_cooldown = 0

    def update_path(self, player_pos, mapping):
        grid_matrix = [[0 if cell == 0 else 1 for cell in row] for row in mapping]
        grid = Grid(matrix=grid_matrix)
        start = grid.node(self.rect.x // (WIDTH // len(mapping[0])), self.rect.y // (HEIGHT // len(mapping)))
        end = grid.node(player_pos[0] // (WIDTH // len(mapping[0])), player_pos[1] // (HEIGHT // len(mapping)))
        finder = AStarFinder()
        self.path, _ = finder.find_path(start, end, grid)

    def move_towards_player(self):
        if self.move_cooldown > 0 or not self.path:
            self.move_cooldown -= 1
            return

        next_pos = self.path.pop(0)
        self.rect.x = next_pos[0] * (WIDTH // len(mapping[0]))
        self.rect.y = next_pos[1] * (HEIGHT // len(mapping))
        self.move_cooldown = 10