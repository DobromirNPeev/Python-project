import pygame
from Button import Button
from ScreenMixin import ScreenMixin
from Constants import screen_width,screen_height
from Multiplayer.PregameScreenMultiplayer import PregameScreenMutliplayer
from Singleplayer.PregameScreenSingleplayer import PregameScreenSingleplayer
from AddQuestion.AddQuestionScreen import AddQuestionScreen

WHITE = (255, 255, 255)

class MainMenu(ScreenMixin):
    def __init__(self,player):
        super().__init__()
        self.singleplayer = Button(screen_width//2,screen_height//2-50,200,50,"Singleplayer",lambda : PregameScreenSingleplayer(self.player))
        multiplayer = Button(screen_width//2,screen_height//2+25,200,50,"Multiplayer",lambda : PregameScreenMutliplayer())
        add_quesiton = Button(screen_width//2,screen_height//2+100,200,50,"Add question",lambda : AddQuestionScreen())
        exit = Button(screen_width//2,screen_height//2+175,200,50,"Exit",lambda: pygame.quit())
        self.buttons=[self.singleplayer,multiplayer,add_quesiton,exit]
        self.player = player