import pygame
from Constants import screen_width,screen_height

class ScreenMixin:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        pygame.display.set_caption("Pygame Screen Example")

    def render(self,screen):
        pass