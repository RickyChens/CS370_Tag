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


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.has_collided = False  # Flag to check if collision has occurred

    def update(self, player):
        # Check if the obstacle is colliding with the player's hitbox
        if player.hitbox.colliderect(self.rect) and not self.has_collided:
            print("Collision")
            collision_sound.play()
            self.has_collided = True  # Set the flag to True to avoid repeated collisions
        elif not player.hitbox.colliderect(self.rect):
            self.has_collided = False  # Reset the collision flag if not colliding

player = Player(250, 250, 25, 25)
obstacle = Obstacle(100, 100, 25, 25)

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

    player.hitbox.topleft = (player.rect.x - 25, player.rect.y - 25)
    player.rect.clamp_ip(screen_boundaries)
    obstacle.update(player)
    screen.fill(BLACK)

    # Draw player hitbox
    pygame.draw.rect(screen, player.hitbox_color, player.hitbox, 2)

    screen.blit(player.image, player.rect)
    screen.blit(obstacle.image, obstacle.rect)
    pygame.display.flip()
    clock.tick(500)

pygame.quit()
