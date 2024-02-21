from Constants import BLACK,WHITE
from TextBoxBase import TextBoxBase
import copy
import pygame

class TextBoxForFiles(TextBoxBase):
    def __init__(self, x, y, width, height,name,data):
        super().__init__(x, y, width, height)
        self.name = name
        self.data = data

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WHITE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if isinstance(self.data[self.name],list):
                        self.data[self.name].append(self.text)
                    else:
                        self.data[self.name] = copy.deepcopy(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, BLACK)