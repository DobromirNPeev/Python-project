import pygame
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Button:

    def __init__(self, x, y, width, height, text, action):
        self.x,self.y=x,y
        self.width,self.height=width,height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def update_dimensions(self):
        text_surface = self.font.render(self.text, True, BLACK)  # Set a minimum height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height+text_surface.get_height())
    
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        if not self.text:
            return
        words = self.text.split()
        current_line = words[0]
        lines=[]
        for word in words[1:]:
            test_line = current_line + " " + word
            test_surface = self.font.render(test_line, True, BLACK)
            if test_surface.get_width() <= self.width - 20:  # Subtract padding
                current_line = test_line
            else:
                self.update_dimensions()
                lines.append(current_line)
                current_line = word
              #  self.update_dimensions()

        y_offset= self.y+20
        lines.append(current_line)
        for line in lines:
            text_surface = self.font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += self.font.get_height() + 2

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action()