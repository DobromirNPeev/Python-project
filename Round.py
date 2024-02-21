from Button import Button
from Constants import screen_height,screen_width,TERMINATED,VALID,SKIPPED,WHITE
from TimeCountdown import TimeCountdown
from LoadFiles import LoadFiles
from ScreenMixin import ScreenMixin
from InvalidArgumentException import InvalidArgumentException
from abc import ABC, abstractmethod
import random
import pygame


class Round(ScreenMixin, ABC):

    def __init__(self,questions_path, next_round,points_for_round, time_for_round, question_for_round,*args):
        from MainMenu import MainMenu
        from Player import Player
        super().__init__()
        self.loaded_data = LoadFiles.load_questions(questions_path)
        if len(args) == 1:
            self.player = args[0]
            self.player_score = None
            self.current_player=self.player
        elif len(args) == 2:
            self.player1 = args[0]
            self.player2 = args[1]
            self.player1_score = None
            self.player2_score=None
            self.current_player=None
        else:
            raise IndexError("Too many players")
        self.continue_button = Button(screen_width//2-420,screen_height//2-60,200,50,"Continue",next_round)
        self.go_back = Button(screen_width//2-420,screen_height//2,200,50,"Go back",lambda : MainMenu(Player()))
        self.offset_upper_half,self.offset = 260,260
        self.answers = []
        self.buttons = [self.continue_button,self.go_back]
        self.generated_questions = 0
        self.points_for_round = points_for_round
        self.time_for_round = time_for_round
        self.question_for_round = question_for_round
    
    def _choose_random_question(self,questions):
        if not questions or not isinstance(questions,list):
            raise IndexError

        random_index = random.randrange(len(questions))
        return questions.pop(random_index)
    
    def _is_correct(self,answer,correct_answers):
        if not isinstance(correct_answers,list) or not isinstance(answer,str):
            raise InvalidArgumentException
        is_correct_answer=False
        for correct_answer in correct_answers:
            is_correct_answer = answer.lower() == correct_answer.lower()
            if is_correct_answer:
                return True
        return False
    
    def _save_answer(self,correct_answer):
        if not isinstance(correct_answer,list):
            raise InvalidArgumentException
        
        if self.generated_questions<5:
            if len(self.answers)%5!=0:
                self.offset-=self.answers[-1].rect.height+15
            self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
        else:
            if len(self.answers)%5!=0:
                self.offset_upper_half-=self.answers[-1].rect.height+15
            self.answers.append(Button(screen_width//2+185,screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
    
    def _render_intermediate_screen(self,screen):
        if not isinstance(screen,pygame.surface.Surface):
            raise InvalidArgumentException
        if not self.player_score:
                self.player_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.player.points}",lambda : None)
                self.buttons.append(self.player_score)
        ScreenMixin.render(self,screen)
        for answer in self.answers:
            answer.draw(screen)
    
    @abstractmethod
    def _create_interface(self):
        pass
    
    def _render_interface(self,screen):
        if not isinstance(screen,pygame.surface.Surface):
            raise InvalidArgumentException
        screen.blit(self.background, (0, 0))
        for object in self.objects:
            object.draw(screen)
    
    def _check_for_correct_answer(self):
         if self.found_answer is True:
            self.current_player.correct_answer(self.points_for_round)
            return True
         return False
        
    def _handle_events(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return TERMINATED
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.skip_button.rect.collidepoint(event.pos):
                        return SKIPPED
            self.found_answer=self.type_area.handle_event(event)
        return VALID

    def render(self,screen):
        if not isinstance(screen,pygame.surface.Surface):
            raise InvalidArgumentException
        if hasattr(self,'sound') and self.sound is not None:
            self.sound.stop()
        screen.fill(WHITE)
        if self.generated_questions<self.question_for_round:
                self.random_question = self._choose_random_question(self.loaded_data)
                self.correct_answers = self.random_question["answer(s)"]
                self._save_answer(self.correct_answers)
                self._create_interface()
                self.timer = TimeCountdown(self.time_for_round,screen)
                while True:
                    events = pygame.event.get()
                    result = self._handle_events(events)
                    if result is TERMINATED:
                        return
                    elif result is SKIPPED:
                        break
                    self.timer.tick()
                    if not self.timer:
                        break
                    self._render_interface(screen)
                    self.timer.draw_countdown()
                    pygame.display.flip()

                    if self._check_for_correct_answer():
                        break
        else:
            self._render_intermediate_screen(screen)
    