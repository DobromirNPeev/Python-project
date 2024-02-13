from typing import override
from FifthRound import Round
from Button import Button
from Constants import screen_height,screen_width

class MultiplayerRound(Round):
    
    def __init__(self,questions_path,next_round,points_for_round,time_for_round,question_for_round,*args):
        super().__init__(questions_path,next_round,points_for_round,time_for_round,question_for_round,*args)
        self.half=self.question_for_round//2

    def _save_answer(self, correct_answer):
        if self.generated_questions<self.half:
            if len(self.answers)%self.half!=0:
                self.offset-=self.answers[-1].rect.height+15
            self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
            self.current_player=self.player1
        else:
            if len(self.answers)%self.half!=0:
                self.offset_upper_half-=self.answers[-1].rect.height+15
            self.answers.append(Button(screen_width//2+185,screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
            self.current_player=self.player2

    @override
    def _render_intermediate_screen(self,screen):
        if not self.player1_score and not self.player2_score:
                self.player1_score =  Button(screen_width//2-420,screen_height//2-240,200,50,f"{self.player1.name}'s score: {self.player1.points}",lambda : None)
                self.player2_score =  Button(screen_width//2-420,screen_height//2-150,200,50,f"{self.player2.name}'s score: {self.player2.points}",lambda : None)
        screen.blit(self.background, (0, 0))
        self.continue_button.draw(screen)
        self.player1_score.draw(screen)
        self.player2_score.draw(screen)
        for answer in self.answers:
            answer.draw(screen)