import pygame
PINK = (212, 92, 114)


class Button:
    """
        A class representing a Button.

        Attributes
        ----------
        color : tuple
            A tuple (R, G, B) representing the RGB color of the button.
        x : int
            The X-coordinate of the top-left corner of the button.
        y : int
            The Y-coordinate of the top-left corner of the button.
        width : int
            The width of the button.
        height : int
            The height of the button.
        text : str, optional
            The text displayed on the button, defaults to an empty string.

        Methods
        -------
        draw(screen)
            Draws the button on the given Pygame screen.
        is_over(pos)
            Checks if the button is being hovered over given the mouse position.
        """

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text != '':
            font = pygame.font.SysFont('Arial', 40)
            text = font.render(self.text, True, PINK)
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height