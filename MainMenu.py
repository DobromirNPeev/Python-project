from typing import override
import pygame
from Button import Button
from Round import FirstRound
from User import User
from AddQuestions import AddQuestionScreen
from Multiplayer import PreScreenMutliplayer
from ScreenMixin import ScreenMixin
from Constants import screen_width,screen_height

WHITE = (255, 255, 255)

def getMidPoint(x,y,x1,y1):
        return [(x + x1) / 2.0,(y + y1) / 2.0]


class MainMenu(ScreenMixin):
    def __init__(self,user):
        super().__init__()
        midPoint=getMidPoint(0,0,800,600)
        self.singleplayer = Button(midPoint[0],midPoint[1]-50,200,50,"Singleplayer",lambda : self.generate_screen())
        multiplayer = Button(midPoint[0],midPoint[1]+25,200,50,"Multiplayer",lambda : PreScreenMutliplayer())
        add_quesiton = Button(midPoint[0],midPoint[1]+100,200,50,"Add question",lambda : self.generated_add_question_screen())
        exit = Button(midPoint[0],midPoint[1]+175,200,50,"Exit",lambda: pygame.quit())
        self.buttons=[self.singleplayer,multiplayer,add_quesiton,exit]
        self.user = user

    def generated_add_question_screen(self):
        return AddQuestionScreen()

    def generate_screen(self):
        return PreGameScreen(self.user)
    
    @override
    def render(self, screen):
        # Draw background
        self.screen.fill(WHITE)
        screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(screen)

class PreGameScreen(ScreenMixin):
    def __init__(self,user):
        super().__init__()
        midPoint=getMidPoint(0,0,800,600)
        self.start = Button(midPoint[0],midPoint[1]-50,200,50,"Start",lambda : self.start_game())
        self.go_back = Button(midPoint[0],midPoint[1]+25,200,50,"Go back",lambda : self.generate_menu())
        self.buttons=[self.start,self.go_back]
        self.user = user
    
    def generate_menu(self):
        return MainMenu(self.user)

    def start_game(self):
        clock = pygame.time.Clock()
        timer_duration = 1000 
        elapsed_time = 0 
        font = pygame.font.Font(None, 36)
        while True:
            dt = clock.tick(60)  # Adjust the argument based on your desired frame rate
            elapsed_time += dt

            # Calculate remaining time
            remaining_time = max(timer_duration - elapsed_time, 0)

            # Convert remaining time to seconds
            remaining_seconds = remaining_time // 1000
            if remaining_seconds<=0:
                break
            self.screen.blit(self.background, (0, 0))
            timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2))
            self.screen.blit(timer_text, timer_rect)
            pygame.display.flip()
        return FirstRound(self.user)
    
    @override
    def render(self, screen):
        # Draw background
        self.screen.fill(WHITE)
        screen.blit(self.background, (0, 0))
        self.start.draw(screen)
        self.go_back.draw(screen)