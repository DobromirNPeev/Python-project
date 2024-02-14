from Button import Button
from TextBox.TextBoxForMultiplayer import TextBoxForMultiplayer
from Player import Player
from ScreenMixin import ScreenMixin
from Constants import *
from TimeCountdown import TimeCountdown
from Multiplayer.FirstRoundMultiplayer import FirstRoundMultiplayer

class PregameScreenMutliplayer(ScreenMixin):

    def __init__(self):
        from MainMenu import MainMenu
        from Player import Player
        super().__init__()
        self.user1=Player()
        self.user2=Player()
        self.enter_player1_name=Button(screen_width//2-100,screen_height//2-150,300,50,"Player 1 enter name:",lambda: None)
        self.enter_player1_textbox=TextBoxForMultiplayer(screen_width // 2-100, screen_height // 2-90,250,35,self.user1)
        self.enter_player2_name=Button(screen_width//2-100,screen_height//2-40,300,50,"Player 2 enter name:",lambda: None)
        self.enter_player2_textbox=TextBoxForMultiplayer(screen_width // 2-100, screen_height // 2+20,250,35,self.user2)
        self.ready=Button(screen_width//2-100,screen_height//2+80,200,50,"Ready",lambda: self.start_game())
        self.go_back = Button(screen_width//2-100,screen_height//2+140,200,50,"Go back",lambda : MainMenu(Player()))
        self.buttons=[self.enter_player1_name,self.enter_player1_textbox,self.enter_player2_name,self.enter_player2_textbox,self.ready,self.go_back]

    def start_game(self):
        self.timer=TimeCountdown(5000,self.screen)
        self.timer.start_clock(self.background)
        return FirstRoundMultiplayer(self.user1,self.user2)    
