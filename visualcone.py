import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
w, h = 800, 600
backgroundimg = "background.jpg"
player_color = (255, 255, 0)
obj_color = (255, 255, 255)
light_lvl = 1500  # Adjust this to control the intensity of the flashlight
player_spd = 5
rotation_angle = 5  # Angle of rotation in degrees
visible_distance = 300  # Maximum distance the flashlight illuminates

# Function to draw flashlight mask
def draw_flashlight_mask(surface, player_pos, cone_angle):
    cone_mask = pygame.Surface((w, h), pygame.SRCALPHA)
    cone_mask.fill((0, 0, 0))  # Fill with transparent color

    # Calculate flashlight cone vertices
    vertices = [
        player_pos,
        (
            player_pos[0] + math.cos(math.radians(cone_angle + 30)) * visible_distance,
            player_pos[1] - math.sin(math.radians(cone_angle + 30)) * visible_distance
        ),
        (
            player_pos[0] + math.cos(math.radians(cone_angle - 30)) * visible_distance,
            player_pos[1] - math.sin(math.radians(cone_angle - 30)) * visible_distance
        )
    ]
    pygame.draw.polygon(cone_mask, (0, 0, 0, 200), vertices)

    surface.blit(cone_mask, (0, 0))

# Function to draw objects
def draw_objects(screen, player_pos):
    object_pos = [(400, 300), (600, 200), (200, 400)]  # Example object positions

    for obj in object_pos:
        distance_to_player = math.hypot(obj[0] - player_pos[0], obj[1] - player_pos[1])
        if distance_to_player <= visible_distance:
            brightness = max(0, min(light_lvl - (distance_to_player / visible_distance * light_lvl), 255))
            pygame.draw.circle(screen, (brightness, brightness, brightness), obj, 20)

# Main function
def main():
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Flashlight Effect")

    background_image = pygame.image.load(backgroundimg).convert()  # Load background image
    background_image = pygame.transform.scale(background_image, (w, h))  # Scale to fit screen

    player_pos = [100, 100]  # Example player position
    cone_angle = 0  # Initial flashlight angle

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game is being closed.")
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cone_angle += rotation_angle
        if keys[pygame.K_RIGHT]:
            cone_angle -= rotation_angle
        if keys[pygame.K_UP]:
            # Calculate movement vector based on player angle
            move_x = math.cos(math.radians(cone_angle))
            move_y = -math.sin(math.radians(cone_angle))
            player_pos[0] += move_x * player_spd
            player_pos[1] += move_y * player_spd
        if keys[pygame.K_DOWN]:
            # Calculate movement vector based on player angle (move backwards)
            move_x = -math.cos(math.radians(cone_angle))
            move_y = math.sin(math.radians(cone_angle))
            player_pos[0] += move_x * player_spd
            player_pos[1] += move_y * player_spd

        screen.blit(background_image, (0, 0))  # Draw background image
        draw_objects(screen, player_pos)
        draw_flashlight_mask(screen, player_pos, cone_angle)
        pygame.draw.circle(screen, player_color, player_pos, 10)  # Draw the player
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()