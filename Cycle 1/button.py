import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 800))
main_font = pygame.font.SysFont("cambria", 50)


class Button:
    def __init__(self, image, pos, text_input):
        self.image = image
        self.pos = pos
        self.text = main_font.render(text_input, True, "white")
        self.rect = self.image.get_rect(center=pos)
        self.text_rect = self.text.get_rect(center=pos)

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            print("Clicked")


button = Button(pygame.Surface([200, 80]), (250, 250), "Button")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            button.checkInput(pygame.mouse.get_pos())

    screen.fill("white")

    button.draw()
    pygame.display.update()
