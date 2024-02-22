import pygame
import random
from constants import *

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
screen_boundaries = pygame.Rect((0, 0), (HEIGHT, WIDTH))

PLAYER_SIZE = 20  # Adjust player size


def generate_random_map():
    map_grid = [[1 for _ in range(15)] for _ in range(15)]  # Increase map size

    def is_valid_cell(x, y):
        return 0 <= x < 15 and 0 <= y < 15

    def backtrack(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + 2 * dx, y + 2 * dy
            if is_valid_cell(new_x, new_y) and map_grid[new_x][new_y] == 1:
                map_grid[new_x][new_y] = 0
                map_grid[x + dx][y + dy] = 0
                backtrack(new_x, new_y)

    start_x, start_y = random.randint(0, 7) * 2, random.randint(0, 7) * 2
    map_grid[start_x][start_y] = 0
    backtrack(start_x, start_y)

    # Introduce more randomness by breaking some walls
    for i in range(15):
        for j in range(15):
            if random.random() < 0.6:  # Adjust probability for openness
                map_grid[i][j] = 0

    # Check for dead ends and convert them into corridors
    for i in range(15):
        for j in range(15):
            if map_grid[i][j] == 0:
                neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                num_openings = sum(1 for x, y in neighbors if is_valid_cell(x, y) and map_grid[x][y] == 0)
                if num_openings == 1:
                    map_grid[i][j] = 0  # Convert dead end into corridor

    return map_grid


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()

        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

    def randomSpawn(self):
        while True:
            x = random.randint(0, WIDTH - PLAYER_SIZE)
            y = random.randint(0, HEIGHT - PLAYER_SIZE)
            new_rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

            # Check for collision with obstacles
            if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
                self.rect.topleft = (x, y)
                break

    def move(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        for obstacle in obstacles:
            if new_rect.colliderect(obstacle):
                return  # Stop moving if collision occurs

        # Move the player if no collision occurs
        self.rect.move_ip(dx, dy)


obstacles = []
mapping = generate_random_map()
for r in range(len(mapping)):
    for c in range(len(mapping[r])):
        if mapping[r][c] == 1:
            obstacle = pygame.Rect(c * (WIDTH // len(mapping[r])),
                                   r * (HEIGHT // len(mapping)),
                                   WIDTH // len(mapping[r]),
                                   HEIGHT // len(mapping))
            obstacles.append(obstacle)

# Generate player position not inside walls`
player_position = (0, 0)


player = Player(player_position, WHITE)
player.randomSpawn()
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dx, dy = 0, 0

    if keys[pygame.K_LEFT]:
        player.move(-2, 0)
    if keys[pygame.K_RIGHT]:
        player.move(2, 0)
    if keys[pygame.K_UP]:
        player.move(0, -2)
    if keys[pygame.K_DOWN]:
        player.move(0, 2)

    player.move(dx, dy)

    screen.fill(BLACK)
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    player.rect.clamp_ip(screen_boundaries)
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
