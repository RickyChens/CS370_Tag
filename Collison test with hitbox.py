import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
screen_boundaries = pygame.Rect((0, 0), (HEIGHT, WIDTH))

# Initialize the mixer module
pygame.mixer.init()

# Load the sound file
collision_sound = pygame.mixer.Sound("sound.wav")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Adjust hitbox dimensions and color
        self.hitbox = pygame.Rect(x - 25, y - 25, width + 50, height + 50)
        self.hitbox_color = WHITE  # New line to set hitbox color

    def update(self):
        # Update the hitbox position to match the player's position
        self.hitbox.topleft = (self.rect.x - 25, self.rect.y - 25)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.has_collided = False  # Flag to check if collision has occurred

    def update(self):
        # Check if the obstacle is colliding with the player's hitbox
        if player.hitbox.colliderect(self.rect) and not self.has_collided:
            print("Collision")
            collision_sound.play()
            self.has_collided = True  # Set the flag to True to avoid repeated collisions

player = Player(250, 250, 25, 25)
obstacle = Obstacle(100, 100, 25, 25)

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
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1

    new_rect = player.rect.move(dx, dy)

    # Update hitbox position to match the player's position
    player.hitbox.topleft = (new_rect.x - 25, new_rect.y - 25)

    obstacle.update()
    if not new_rect.colliderect(obstacle.rect):
        player.rect = new_rect
    else:
        obstacle.has_collided = False  # Reset the collision flag if not colliding

    player.rect.clamp_ip(screen_boundaries)

    screen.fill(BLACK)

    # Draw player hitbox
    pygame.draw.rect(screen, player.hitbox_color, player.hitbox, 2)

    screen.blit(player.image, player.rect)
    screen.blit(obstacle.image, obstacle.rect)
    pygame.display.flip()
    clock.tick(500)

pygame.quit()
