import sys

import pygame

from LfsConnection import LFSConnection


class PACTDrivingAssistant2:

    def __init__(self):
        pygame.init()  # initialize pygame
        pygame.mixer.init()
        pygame.display.set_caption('Pact Driving Assistant 2')
        self.width, self.height = 800, 600
        self.btn_width, self.btn_height = 110, 50
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.icon = pygame.image.load('data\\images\\icon.png')
        pygame.display.set_icon(self.icon)
        self.colors = {
            "WHITE": (255, 255, 255),
            "RED": (255, 204, 204),
            "BLUE": (180, 210, 228),
            "GREEN": (204, 255, 204),
            "ORANGE": (255, 204, 153),
            "DARK_ORANGE": (220, 160, 120),
            "GREY": (60, 60, 60),
            "PURPLE": (41, 14, 63),
            "PINK": (212, 92, 114),
        }

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

        elif event.type == pygame.KEYDOWN:
            pass

    def quit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def run(self):
        lfs_connection = LFSConnection()
        lfs_connection.run()
        while self.running:
            self.screen.fill(self.colors['GREY'])
            for event in pygame.event.get():
                self.handle_event(event)
            pygame.display.update()


if __name__ == "__main__":
    pda = PACTDrivingAssistant2()
    pda.run()
