import pygame
import sys

def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def main():
    pygame.init()

    # Set the screen size
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Click Sound Example')

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Replace 'click_sound.wav' with the path to your sound file
                play_sound("soundwhoosh.wav")

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
