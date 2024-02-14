import pygame
from Constants import BLACK,WHITE
from TextBox.TextBoxBase import TextBoxBase

class TextBoxForQuestions(TextBoxBase):
    def __init__(self, x, y, width, height,action,correct_answer):
        super().__init__(x,y,width,height)
        self.action=action
        self.correct_answer=correct_answer

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the text box, it becomes active
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WHITE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    found_answer=self.action(self.text,self.correct_answer)
                    print(self.text)
                    self.text = ''
                    self.txt_surface = self.font.render(self.text, True, BLACK)
                    return found_answer
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, BLACK)