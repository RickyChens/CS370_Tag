class Button:
    def __init__(self, image, pos, text_input, font):
        self.image = image
        self.pos = pos
        self.text = font.render(text_input, True, "white")
        self.rect = self.image.get_rect(center=pos)
        self.text_rect = self.text.get_rect(center=pos)
        self.pressed = False

    def draw(self, screen):
        if self.pressed:
            self.image.fill((0, 0, 0))  # Fill the image with green color
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.pressed = not self.pressed  # Toggle the pressed attribute
            return True