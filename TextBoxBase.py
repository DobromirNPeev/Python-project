import pygame
from Constants import BLACK,screen_width
from abc import ABC, abstractmethod

class TextBoxBase(ABC):
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x,self.y,self.initial_width,self.initial_height = x, y , width, height
        self.color = BLACK
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.text, True, BLACK)
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (192, 192, 192), self.rect)
        txt_surface = self.font.render(self.text, True, BLACK)
        if txt_surface.get_width() < screen_width - self.x:
            text_width = max(txt_surface.get_width() + 10, self.initial_width)
        else:
            text_width = screen_width - self.x - 5
            self.text = self.text[:-1]
        self.rect.size = (text_width, self.initial_height)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    @abstractmethod
    def handle_event(self):
        pass

