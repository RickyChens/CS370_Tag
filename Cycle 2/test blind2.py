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
NUM_CIRCLES = 40    # Number of concentric circles
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

    # Draw the concentric circles
    init_radius = 100
    radius_step = (800 - init_radius) // NUM_CIRCLES

    for i in range(NUM_CIRCLES):
        circle_radius = init_radius + i * radius_step
        alpha = 255 - i * (255 // NUM_CIRCLES)  # Smoothly decrease alpha from inner to outer circles
        pygame.draw.circle(screen, (0, 0, 0, alpha), player_pos, circle_radius, width=1)  # Set width to 1 to make sure circles are visible

    # Draw the player circle
    pygame.draw.circle(screen, BLACK, player_pos, PLAYER_RADIUS)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
