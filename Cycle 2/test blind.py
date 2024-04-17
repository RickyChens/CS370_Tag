import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_RADIUS = 30  # Radius of the player circle
NUM_CIRCLES = 30    # Number of concentric circles
CIRCLE_RADIUS_STEP = 10  # Step for increasing the radius of each circle
CIRCLE_RADIUS = 120  # Radius of the innermost circle

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Main game loop
player_pos = [WIDTH // 2, HEIGHT // 2]  # Player position
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player position (for testing, you would likely have player movement code here)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player circle
    initRadius = 100
    radius = (800-initRadius)//40

    for i in range(40):
        alpha = 255/50
        circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(circle, (0, 0, 0, alpha*i), (player_pos[0], player_pos[1]), radius*i, radius)
        screen.blit(circle, (0, 0))

    # Draw multiple concentric circles around the player
    # for i in range(1, NUM_CIRCLES + 1):
    #     circle_radius = CIRCLE_RADIUS + i * CIRCLE_RADIUS_STEP
    #     opacity = int(255 * (1 - i / NUM_CIRCLES))  # Calculate opacity based on radius
    #     pygame.draw.circle(screen, (0, 0, 0, opacity), player_pos, circle_radius)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()