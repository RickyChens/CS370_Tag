import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Empty Pygame Program")

initRadius = 100
radius = (800 - initRadius) // 100
circle_surface = pygame.Surface((radius * 23 * 2, radius * 23 * 2), pygame.SRCALPHA)
for i in range(23):
    alpha = 255 / 100
    circle = pygame.Surface((radius * 23 * 2, radius * 23 * 2), pygame.SRCALPHA)
    circle_center = (radius * 23, radius * 23)
    pygame.draw.circle(circle, (0, 0, 0, int(alpha * i)), circle_center, radius * i, radius)
    circle_surface.blit(circle, (0, 0))  # Blit the circle onto circle_surface

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((223, 115, 255))

    # Blit the circle_surface onto the screen
    screen.blit(circle_surface, (0 - 161, 0 - 161))

    # Update the display
    pygame.display.flip()
