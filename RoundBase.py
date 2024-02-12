from Button import Button
from Constants import screen_height,screen_width,TERMINATED,VALID,SKIPPED
import random
import pygame
from LoadFiles import LoadFiles
from ScreenMixin import ScreenMixin

class Round(ScreenMixin):

    def __init__(self,questions_path,user,next_round):
        super().__init__()
        self.loaded_data = LoadFiles.load_questions(questions_path)
        self.user = user
        self.continue_button = Button(screen_width//2-420,screen_height//2-60,200,50,"Continue",next_round)
        self.offset_upper_half,self.offset=260,260
        self.answers=[]
        self.user_score = None
        self.buttons=[self.continue_button]
        self.generated_questions=0
    
    def _choose_random_question(self,questions):
        if not questions:
            return None

        random_index = random.randrange(len(questions))
        return questions.pop(random_index)
    
    def _is_correct(self,answer,correct_answers):
        is_correct_answer=False
        for correct_answer in correct_answers:
            is_correct_answer = answer.lower() == correct_answer.lower()
            if is_correct_answer:
                return True
        return False
    
    def _save_answer(self,correct_answer):
        if self.generated_questions<5:
            if len(self.answers)%5!=0:
                self.offset-=self.answers[-1].rect.height+15
            self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
        else:
            if len(self.answers)%5!=0:
                self.offset_upper_half-=self.answers[-1].rect.height+15
            self.answers.append(Button(screen_width//2+185,screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
    
    def _render_intermediate_screen(self,screen):
        if not self.user_score:
                self.user_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.user.points}",lambda : None)
                self.buttons.append(self.user_score)
        ScreenMixin.render(self,screen)
        for answer in self.answers:
            answer.draw(screen)
    
    def _create_interface(self,random_question):
        from textbox import TextBoxForQuestions
        self.random_question = random_question
        self.question_text = Button(screen_width // 2-222, screen_height // 2,500,50,random_question['question'],lambda: None)
        self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,random_question["answers"])
        self.skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,"Skip",lambda: None)
        self.objects=[self.question_text,self.skip_button,self.type_area]
        self.found_answer = None
        self.generated_questions+=1
    
    def _render_interface(self,screen):
        screen.blit(self.background, (0, 0))
        for object in self.objects:
            object.draw(screen)
    
    def _check_for_correct_answer(self,points):
         if self.found_answer is True:
            self.user.correct_answer(points)
            print(self.user.points)
            return True
        
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

    