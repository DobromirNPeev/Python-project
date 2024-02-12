from typing import override
import pygame
from Button import Button
from Round import FirstRound
from User import User
from AddQuestions import AddQuestionScreen
from Multiplayer import PreScreenMutliplayer
from ScreenMixin import ScreenMixin
from Constants import screen_width,screen_height
from TimeCountdown import TimeCountdown

WHITE = (255, 255, 255)

class MainMenu(ScreenMixin):
    def __init__(self,user):
        super().__init__()
        self.singleplayer = Button(screen_width//2,screen_height//2-50,200,50,"Singleplayer",lambda : PreGameScreen(self.user))
        multiplayer = Button(screen_width//2,screen_height//2+25,200,50,"Multiplayer",lambda : PreScreenMutliplayer())
        add_quesiton = Button(screen_width//2,screen_height//2+100,200,50,"Add question",lambda : AddQuestionScreen())
        exit = Button(screen_width//2,screen_height//2+175,200,50,"Exit",lambda: pygame.quit())
        self.buttons=[self.singleplayer,multiplayer,add_quesiton,exit]
        self.user = user
    

class PreGameScreen(ScreenMixin):
    def __init__(self,user):
        super().__init__()
        self.start = Button(screen_width//2,screen_height//2-50,200,50,"Start",lambda : self.start_game())
        self.go_back = Button(screen_width//2,screen_height//2+25,200,50,"Go back",lambda : MainMenu(self.user))
        self.buttons=[self.start,self.go_back]
        self.user = user

    def start_game(self):
        self.timer=TimeCountdown(5000,self.screen)
        while True:
            self.timer.tick()
            if not self.timer:
                break
            self.screen.blit(self.background, (0, 0))
            self.timer.draw_countdown()
            pygame.display.flip()
        return FirstRound(self.user)