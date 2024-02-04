import pygame

# Define colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Define screen size
WIDTH = 640
HEIGHT = 480

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Dot")
clock = pygame.time.Clock()

# Create the dot sprite
dot_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)

# Game loop
running = True

while running:
    # Check for events


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()

    # Move the dot based on key presses
    move_x = 0
    move_y = 0
    if keys[pygame.K_LEFT]:
        move_x -= 5

    if keys[pygame.K_RIGHT]:
        move_x += 5

    if keys[pygame.K_UP]:
        move_y -= 5

    if keys[pygame.K_DOWN]:
        move_y += 5

        # Update the dot's position
    dot_rect.move_ip(move_x, move_y)

    # Don't allow the dot to go off the screen
    dot_rect.clamp_ip(screen.get_rect())

    # Draw the screen
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, dot_rect)
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()