import pygame
from Constants import BLACK

class TextBoxBase:
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.text, True, BLACK)
        self.active = False
    
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, (192, 192, 192), self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    def handle_event(self):
        pass

