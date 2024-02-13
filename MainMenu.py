from typing import override
import pygame
from Button import Button
from FifthRound import FirstRound
from AddQuestions import AddQuestionScreen
from Multiplayer import PreScreenMutliplayer
from ScreenMixin import ScreenMixin
from Constants import screen_width,screen_height,TIME_FOR_LOADING_SCREEN
from TimeCountdown import TimeCountdown

WHITE = (255, 255, 255)

class MainMenu(ScreenMixin):
    def __init__(self,player):
        super().__init__()
        self.singleplayer = Button(screen_width//2,screen_height//2-50,200,50,"Singleplayer",lambda : PreGameScreen(self.player))
        multiplayer = Button(screen_width//2,screen_height//2+25,200,50,"Multiplayer",lambda : PreScreenMutliplayer())
        add_quesiton = Button(screen_width//2,screen_height//2+100,200,50,"Add question",lambda : AddQuestionScreen())
        exit = Button(screen_width//2,screen_height//2+175,200,50,"Exit",lambda: pygame.quit())
        self.buttons=[self.singleplayer,multiplayer,add_quesiton,exit]
        self.player = player
    

class PreGameScreen(ScreenMixin):
    def __init__(self,player):
        super().__init__()
        self.start = Button(screen_width//2,screen_height//2-50,200,50,"Start",lambda : self.start_game())
        self.go_back = Button(screen_width//2,screen_height//2+25,200,50,"Go back",lambda : MainMenu(self.player))
        self.buttons=[self.start,self.go_back]
        self.player = player

    def start_game(self):
        self.timer=TimeCountdown(TIME_FOR_LOADING_SCREEN,self.screen)
        self.timer.start_clock(self.background)
        return FirstRound(self.player)