import pygame
from Constants import BLACK,GRAY

class Button:

    def __init__(self, x, y, width, height, text, action):
        self.x,self.y=x,y
        self.width,self.height=width,height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)
        if text:
            words = self.text.split()
            current_line = words[0]
            self.lines=[]
            for word in words[1:]:
                test_line = current_line + " " + word
                test_surface = self.font.render(test_line, True, BLACK)
                if test_surface.get_width() <= self.width - 20:
                    current_line = test_line
                else:
                    self.update_dimensions(current_line,self.lines)
                    self.lines.append(current_line)
                    current_line = word
            self.lines.append(current_line)

    def update_dimensions(self,current_line,lines):
        text_surface = self.font.render(current_line, True, BLACK)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height+text_surface.get_height()+25*len(lines))

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        y_offset= self.y+20
        for line in self.lines:
            text_surface = self.font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += self.font.get_height() + 2

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action()
