from Button import Button
from ScreenMixin import ScreenMixin
from Constants import screen_width,screen_height,TIME_FOR_LOADING_SCREEN
from TimeCountdown import TimeCountdown
from FirstRound import FirstRound

class PregameScreenSingleplayer(ScreenMixin):
    def __init__(self,player):
        from MainMenu import MainMenu
        super().__init__()
        self.start = Button(screen_width//2-100,screen_height//2-50,200,50,"Start",lambda : self.start_game())
        self.go_back = Button(screen_width//2-100,screen_height//2+25,200,50,"Go back",lambda : MainMenu(self.player))
        self.buttons=[self.start,self.go_back]
        self.player = player

    def start_game(self):
        self.timer=TimeCountdown(TIME_FOR_LOADING_SCREEN,self.screen)
        self.timer.start_clock(self.background)
        return FirstRound(self.player)