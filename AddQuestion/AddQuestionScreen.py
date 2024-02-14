from typing import override
from Button import Button
from ScreenMixin import ScreenMixin
from Constants import screen_height,screen_width
from AddQuestion.FirstRoundAddQuestion import FirstRoundAddQuestion
from AddQuestion.SecondRoundAddQuestion import SecondRoundAddQuestion
from AddQuestion.ThirdRoundAddQuestion import ThirdRoundAddQuestion
from AddQuestion.FourthRoundAddQuestion import FourthRoundAddQuestion
from AddQuestion.FifthRoundAddQuestion import FifthRoundAddQuestion

class AddQuestionScreen(ScreenMixin):
        
    def __init__(self):
        from MainMenu import MainMenu
        from Player import Player
        super().__init__()
        self.first_round_question_button = Button(screen_width//2-100,screen_height//2-250,200,50,"First Round Question",lambda : FirstRoundAddQuestion())
        self.second_round_question_button = Button(screen_width//2-100,screen_height//2-160,200,50,"Second Round Question",lambda : SecondRoundAddQuestion())
        self.third_round_question_button = Button(screen_width//2-100,screen_height//2-70,200,50,"Third Round Question",lambda : ThirdRoundAddQuestion())
        self.fourth_round_question_button = Button(screen_width//2-100,screen_height//2+20,200,50,"Fourth Round Question",lambda : FourthRoundAddQuestion())
        self.fifth_round_question_button = Button(screen_width//2-100,screen_height//2+110,200,50,"Fifth Round Question",lambda : FifthRoundAddQuestion())
        self.go_back_button = Button(screen_width//2-100,screen_height//2+210,200,50,"Go back",lambda : MainMenu(Player()))
        self.buttons=[self.first_round_question_button,self.second_round_question_button,self.third_round_question_button,self.fourth_round_question_button,self.fifth_round_question_button,self.go_back_button]
