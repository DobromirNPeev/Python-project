from Button import Button
from TextBoxForMultiplayer import TextBoxForMultiplayer
from Constants import TIME_FOR_LOADING_SCREEN
from ScreenMixin import ScreenMixin
from Constants import *
from TimeCountdown import TimeCountdown
from FirstRoundMultiplayer import FirstRoundMultiplayer

class PregameScreenMutliplayer(ScreenMixin):

    def __init__(self):
        from MainMenu import MainMenu
        from Player import Player
        super().__init__()
        self.player1=Player()
        self.player2=Player()
        self.enter_player1_name=Button(screen_width//2-100,screen_height//2-150,300,50,"Player 1 enter name:",lambda: None)
        self.enter_player1_textbox=TextBoxForMultiplayer(screen_width // 2-100, screen_height // 2-90,250,35,self.player1)
        self.enter_player2_name=Button(screen_width//2-100,screen_height//2-40,300,50,"Player 2 enter name:",lambda: None)
        self.enter_player2_textbox=TextBoxForMultiplayer(screen_width // 2-100, screen_height // 2+20,250,35,self.player2)
        self.ready=Button(screen_width//2-100,screen_height//2+80,200,50,"Ready",lambda: self.start_game())
        self.go_back = Button(screen_width//2-100,screen_height//2+140,200,50,"Go back",lambda : MainMenu(Player()))
        self.buttons=[self.enter_player1_name,self.enter_player1_textbox,self.enter_player2_name,self.enter_player2_textbox,self.ready,self.go_back]

    def start_game(self):
        if self.player1.name == '' or self.player2.name == '':
            return
        self.timer=TimeCountdown(TIME_FOR_LOADING_SCREEN,self.screen)
        self.timer.start_clock(self.background)
        return FirstRoundMultiplayer(self.player1,self.player2)    
