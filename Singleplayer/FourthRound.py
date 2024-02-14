from typing import override
from Button import Button
from Constants import FOURTH_ROUND_QUESTION_PATH,QUESTIONS_FOR_FOURTH_ROUND,POINTS_FOR_FOURTH_ROUND,TIME_FOR_FOURTH_ROUND,screen_height,screen_width
from Singleplayer.Round import Round
from TextBox.TextBoxForQuestions import TextBoxForQuestions
from Singleplayer.FifthRound import FifthRound

class FourthRound(Round):

    def __init__(self,player):
        super().__init__(FOURTH_ROUND_QUESTION_PATH,lambda : FifthRound(player),
                         POINTS_FOR_FOURTH_ROUND,
                         TIME_FOR_FOURTH_ROUND,
                         QUESTIONS_FOR_FOURTH_ROUND,
                         player)
    
    @override
    def _create_interface(self):
        self.needed_answers=self.random_question['needed_answers']
        self.correct_answered=0
        self.question_text = Button(screen_width // 2-230, screen_height // 2-100,500,50,self.random_question['question'],lambda: None)
        self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,self.correct_answers)
        self.skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
        self.objects=[self.question_text,self.skip_button,self.type_area]
        self.found_answer = None
        self.generated_questions+=1
    
    @override
    def _check_for_correct_answer(self):
        if self.found_answer is True:
            self.correct_answered+=1
            self.found_answer = None
            if self.correct_answered == self.needed_answers:
                self.player.correct_answer(self.points_for_round)
                print(self.player.points)
                return True