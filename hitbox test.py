import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hitbox Example")
clock = pygame.time.Clock()

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)

# Create a class for the player character
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Adjust hitbox dimensions
        self.hitbox = pygame.Rect(x - 25, y - 25, width + 50, height + 50)

    def update(self):
        # Update the hitbox position to match the player's position
        self.hitbox.topleft = (self.rect.x - 25, self.rect.y - 25)

# Create the player
player = Player(50, 50, 50, 50)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
    if keys[pygame.K_UP]:
        player.rect.y -= 5
    if keys[pygame.K_DOWN]:
        player.rect.y += 5

    # Draw everything
    screen.fill(white)
    all_sprites.draw(screen)

    player.update()
    # Draw the wider hitbox (optional, for debugging)
    pygame.draw.rect(screen, (0, 255, 0), player.hitbox, 6)

    clock.tick(60)
    pygame.display.flip()

