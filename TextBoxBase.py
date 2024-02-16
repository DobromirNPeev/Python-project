import pygame
from Constants import BLACK
from abc import ABC, abstractmethod

class TextBoxBase(ABC):
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.initial_width,self.initial_height = width,height
        self.color = BLACK
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.text, True, BLACK)
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (192, 192, 192), self.rect)
        txt_surface = self.font.render(self.text, True, BLACK)
        text_width = max(txt_surface.get_width() + 10, self.initial_width)
        text_height = max(txt_surface.get_height() + 10, self.initial_height)
        self.rect.size = (text_width, text_height)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    @abstractmethod
    def handle_event(self):
        pass

