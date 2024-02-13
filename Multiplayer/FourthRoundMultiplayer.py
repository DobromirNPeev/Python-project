from typing import override
from Button import Button
from textbox import TextBoxForQuestions
from Constants import *
from MultiplayerRound import MultiplayerRound

class FourthRoundMultiplayer(MultiplayerRound):

    def __init__(self,player1,player2):
        from FifthRoundMultiplayer import FifthRoundMultiplayer
        super().__init__(FOURTH_ROUND_QUESTION_PATH,lambda : FifthRoundMultiplayer(player1,player2),
                         POINTS_FOR_FOURTH_ROUND,
                         TIME_FOR_FOURTH_ROUND,
                         QUESTIONS_FOR_FOURTH_ROUND,
                         player1,player2)

    @override
    def _create_interface(self):
        self.player_turn=Button(screen_width//2 - 115,screen_height//2 + 225,250,50,f"{self.current_player.name}'s turn",lambda: None)
        self.question_text = Button(screen_width//2 - 230, screen_height//2 - 100,500,50,self.random_question['question'],lambda: None)
        self.type_area = TextBoxForQuestions(screen_width//2 - 115, screen_height//2 + 84,250,35,self._is_correct,self.random_question["answer(s)"])
        self.skip_button= Button(screen_width//2 - 65,screen_height//2 + 125,150,50,f"Skip",lambda: None)
        self.objects=[self.player_turn,self.question_text,self.skip_button,self.type_area]
        self.found_answer = None
        self.generated_questions+=1
        self.needed_answers=self.random_question['needed_answers']
        self.correct_answered=0

    @override
    def _check_for_correct_answer(self):
        if self.found_answer is True:
            self.correct_answered+=1
            self.found_answer = None
            if self.correct_answered == self.needed_answers:
                self.current_player.correct_answer(self.points_for_round)
                return True