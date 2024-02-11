from Button import Button
from Constants import screen_height,screen_width
import random
import pygame

class Round:
    def __init__(self,user,next_round):
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
    
    def _render_intermediate_screen(self):
        if not self.user_score:
                self.user_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.user.points}",lambda : None)
        self.screen.blit(self.background, (0, 0))
        self.continue_button.draw(self.screen)
        self.user_score.draw(self.screen)
        for answer in self.answers:
            answer.draw(self.screen)
    
    def _create_interface(self,random_question):
        from textbox import TextBoxForQuestions
        self.question_text = Button(screen_width // 2-222, screen_height // 2,500,50,random_question['question'],lambda: None)
        self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,random_question["answers"])
        self.skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,"Skip",lambda: None)
        self.found_answer = None
        self.click_skip=False
    
    def _draw_interface(self):
        pass