import pygame
from Constants import screen_width,screen_height,WHITE,BACKGROUND_PATH

class ScreenMixin:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load(BACKGROUND_PATH)
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        pygame.display.set_caption("Test your knowledge")

    def render(self,screen):
        screen.fill(WHITE)
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(screen)