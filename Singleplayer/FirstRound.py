from typing import override
from Button import Button
import pygame
from Constants import FIRST_ROUND_QUESTION_PATH,POINTS_FOR_FIRST_ROUND,TIME_FOR_FIRST_ROUND,QUESTIONS_FOR_FIRST_ROUND,screen_height,screen_width,TERMINATED,VALID,SKIPPED
from Singleplayer.Round import Round
from Singleplayer.SecondRound import SecondRound


class FirstRound(Round):

    def __init__(self,player):
        super().__init__(FIRST_ROUND_QUESTION_PATH,lambda : SecondRound(player),
                         POINTS_FOR_FIRST_ROUND,
                         TIME_FOR_FIRST_ROUND,
                         QUESTIONS_FOR_FIRST_ROUND,
                         player)
    
    @override
    def _create_interface(self):
          self.question_text = Button(screen_width//2-250,screen_height//2-150,750,50,self.random_question['question'],lambda: None)
          choices_A = Button(screen_width//2-350,screen_height//2-75,450,50,f"A) {self.random_question['choices'][0]}",lambda: self._is_correct(self.random_question['choices'][0],self.random_question["answer(s)"]))
          choices_B = Button(screen_width//2+125,screen_height//2-75,450,50,f"B) {self.random_question['choices'][1]}",lambda: self._is_correct(self.random_question['choices'][1],self.random_question["answer(s)"]))
          choices_C = Button(screen_width//2-350,screen_height//2,450,50,f"C) {self.random_question['choices'][2]}",lambda: self._is_correct(self.random_question['choices'][2],self.random_question["answer(s)"]))
          choices_D = Button(screen_width//2+125,screen_height//2,450,50,f"D) {self.random_question['choices'][3]}",lambda: self._is_correct(self.random_question['choices'][3],self.random_question["answer(s)"]))
          self.skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
          self.objects=[choices_A,choices_B,choices_C,choices_D,self.skip_button,self.question_text]
          self.found_answer = None
          self.generated_questions+=1
    
    @override
    def _check_for_correct_answer(self):
        if super()._check_for_correct_answer() or self.found_answer is False:
            return True
    @override   
    def _handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return TERMINATED
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for object in self.objects:
                    if object.rect.collidepoint(event.pos):
                        if object==self.skip_button:
                            return SKIPPED
                        self.found_answer = object.handle_event(event)
                        if self.found_answer is not None:
                            return VALID
        return VALID