from typing import override
from Button import Button
from Player import Player
from Constants import FIFTH_ROUND_QUESTION_PATH,POINTS_FOR_FIFTH_ROUND,TIME_FOR_FIFTH_ROUND,QUESTIONS_FOR_FIFTH_ROUND,screen_height,screen_width
from Singleplayer.Round import Round
from TextBox.TextBoxForQuestions import TextBoxForQuestions

class FifthRound(Round):

    def __init__(self,player):
        from MainMenu import MainMenu
        super().__init__(FIFTH_ROUND_QUESTION_PATH,lambda : MainMenu(Player()),
                         POINTS_FOR_FIFTH_ROUND,
                         TIME_FOR_FIFTH_ROUND,
                         QUESTIONS_FOR_FIFTH_ROUND,
                         player)
    @override
    def _create_interface(self):
         self.question_text = Button(screen_width // 2-230, screen_height // 2-175,500,50,self.random_question['question'],lambda: None)
         self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,self.correct_answers)
         self.skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
         self.objects=[self.question_text,self.skip_button,self.type_area]
         self.found_answer = None
         self.generated_questions+=1