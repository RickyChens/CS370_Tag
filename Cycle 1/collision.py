import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
screen_boundaries = pygame.Rect((0, 0), (HEIGHT, WIDTH))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("soldier.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def move(self, dx, dy, obstacle, player_group):
        if dx != 0 or dy != 0:
            self.move_single_axis(dx, dy, obstacle, player_group)

    def move_single_axis(self, dx, dy, obstacle, player_group):
        steps_x = abs(dx) + 1
        steps_y = abs(dy) + 1

        for i in range(max(steps_x, steps_y)):
            old_rect = self.rect.copy()
            self.rect.x += dx / steps_x
            self.rect.y += dy / steps_y

            if pygame.sprite.spritecollide(obstacle, player_group, False, pygame.sprite.collide_mask):
                self.rect = old_rect
                break


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()

        self.image = pygame.Surface([50, 50])
        self.image.fill(color)
        self.image.set_colorkey((255, 100, 98))

        self.rect = self.image.get_rect(center=pos)


def main():
    player = Player((350, 350))
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

    pygame.quit()


if __name__ == "__main__":
    main()
