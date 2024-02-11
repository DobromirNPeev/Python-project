from typing import override
from Button import Button
import pygame
import random
from textbox import TextBoxForQuestions
from ScreenMixin import ScreenMixin
import User
from Constants import screen_height,screen_width,WHITE
from LoadFiles import LoadFiles

def choose_random_question(questions):
    if not questions:
        return None

    random_index = random.randrange(len(questions))
    return questions.pop(random_index)

class FirstRound(LoadFiles,ScreenMixin):

    def __init__(self,user):
        super().__init__("D:/Python project/firstround.json")
        self._load_questions()
        ScreenMixin.__init__(self)
        self.user = user
        self.continue_button = Button(screen_width//2-420,screen_height//2-60,200,50,"Continue",lambda : self.generate_second_round())
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.user_score = None
        self.buttons=[self.continue_button]
        self.generated_questions=0

    def generate_second_round(self):
        return ImageRound(self.user)

    @staticmethod
    def is_correct(answer,correct_answer):
        return answer==correct_answer
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=choose_random_question(self.loaded_data)
                correct_answer = random_question["correct_answer"]   
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,200,50,f"{self.generated_questions+1}) {correct_answer}",lambda : None))
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2+180,screen_height//2-self.offset_upper_half,200,50,f"{self.generated_questions+1}) {correct_answer}",lambda : None))
                question_text = Button(screen_width//2-250,screen_height//2-150,750,50,random_question['question'],lambda: None)
                choices_A = Button(screen_width//2-350,screen_height//2-75,450,50,f"A) {random_question['choices'][0]}",lambda: self.is_correct(random_question['choices'][0],correct_answer))
                choices_B = Button(screen_width//2+125,screen_height//2-75,450,50,f"B) {random_question['choices'][1]}",lambda: self.is_correct(random_question['choices'][1],correct_answer))
                choices_C = Button(screen_width//2-350,screen_height//2,450,50,f"C) {random_question['choices'][2]}",lambda: self.is_correct(random_question['choices'][2],correct_answer))
                choices_D = Button(screen_width//2+125,screen_height//2,450,50,f"D) {random_question['choices'][3]}",lambda: self.is_correct(random_question['choices'][3],correct_answer))
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                choices_buttons=[choices_A,choices_B,choices_C,choices_D,skip_button]
                clock = pygame.time.Clock()
                timer_duration = 8000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                self.generated_questions+=1
                print(self.generated_questions)
                click_skip=False
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                            for button in choices_buttons:
                                if button.rect.collidepoint(event.pos):
                                    if button==skip_button:
                                        click_skip=True
                                        break
                                    found_answer = button.handle_event(event)
                                    if found_answer is not None:
                                        break
                        if click_skip:
                            break 
                    if not pygame.get_init():
                        return 
                    if click_skip:
                        break
                    dt = clock.tick(60)  # Adjust the argument based on your desired frame rate
                    elapsed_time += dt

                    # Calculate remaining time
                    remaining_time = max(timer_duration - elapsed_time, 0)

                    # Convert remaining time to seconds
                    remaining_seconds = remaining_time // 1000
                    if remaining_seconds<=0:
                        break
                    self.screen.blit(self.background, (0, 0))
                    question_text.draw(self.screen)
                    for button in choices_buttons:
                        button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(1)
                        print(self.user.points)
                        break
                    elif found_answer is False:
                        break
        else:
            if not self.user_score:
                self.user_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.user.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.user_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)


class ImageRound(LoadFiles,ScreenMixin):
    
    def __init__(self,user):
        super().__init__('D:/Python project/images/questionsforimages.json')
        self._load_images("D:/Python project/images")
        ScreenMixin.__init__(self)
       # self.copy_questions=copy.deepcopy(self.image_data)
        self.continue_button = Button(screen_width//2-420,screen_height//2-60,200,50,"Continue",lambda : self.generate_thrid_round())
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.user_score = None
        self.user = user
        self.generated_questions=0
    
    def generate_thrid_round(self):
        return AudioRound(self.user)

    @staticmethod
    def is_correct(answer,correct_answers):
        is_correct_answer=False
        if isinstance(correct_answers,list):
            for correct_answer in correct_answers:
                is_correct_answer = answer.lower() == correct_answer.lower()
                if is_correct_answer:
                    return True
            return False
        return answer.lower() == correct_answers.lower()
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
            for self.generated_questions in range(0,10):
                random_question=choose_random_question(self.image_data)
                correct_answer = random_question["answers"]
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2+185,screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                question_text = Button(screen_width // 2-222, screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self.is_correct,correct_answer)
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 8000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                text=''
                click_skip=False
                print(self.generated_questions)
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if skip_button.rect.collidepoint(event.pos):
                                        click_skip=True
                                        break
                        found_answer=type_area.handle_event(event)
                    if not pygame.get_init():
                        return
                    if click_skip:
                        break
                    dt = clock.tick(60)  # Adjust the argument based on your desired frame rate
                    elapsed_time += dt

                    # Calculate remaining time
                    remaining_time = max(timer_duration - elapsed_time, 0)

                    # Convert remaining time to seconds
                    remaining_seconds = remaining_time // 1000
                    if remaining_seconds<=0:
                        break
                    self.screen.blit(self.background, (0, 0))
                    question_text.draw(self.screen)
                    type_area.draw(self.screen)
                    skip_button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    screen.blit(random_question['image'],random_question['rect'])
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(2)
                        print(self.user.points)
                        break
        else:
            if not self.user_score:
                self.user_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.user.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.user_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)

class AudioRound(LoadFiles,ScreenMixin):

    def __init__(self,user):
        super().__init__('D:/Python project/audio-files/audio-files.json')
        self._load_audio("D:/Python project/audio-files")
        ScreenMixin.__init__(self)
        self.continue_button = Button(screen_width//2-420,screen_height//2-60,200,50,"Continue",lambda : self.generate_fourth_round())
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.user_score=None
        self.user = user
        self.generated_questions=0

    def generate_fourth_round(self):
        return OpenQuestions(self.user)

    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
            for self.generated_questions in range(0,10):
                random_question=choose_random_question(self.audio_data)
                correct_answer = random_question["answers"]
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2+185,screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                question_text = Button(screen_width // 2-222, screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,ImageRound.is_correct,correct_answer)
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 8000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                click_skip = False
                text=''
                audio=random_question['audio']
                print(self.generated_questions)
                pygame.mixer.init()
                sound = pygame.mixer.Sound((audio-20).raw_data)
                sound.play()
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if skip_button.rect.collidepoint(event.pos):
                                        click_skip=True
                                        break
                        found_answer=type_area.handle_event(event)
                    if not pygame.get_init():
                        return
                    if click_skip:
                        break
                    dt = clock.tick(60)
                    elapsed_time += dt
                    remaining_time = max(timer_duration - elapsed_time, 0)
                    remaining_seconds = remaining_time // 1000
                    if remaining_seconds<=0:
                        break
                    self.screen.blit(self.background, (0, 0))
                    question_text.draw(self.screen)
                    type_area.draw(self.screen)
                    skip_button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(3)
                        print(self.user.points)
                        break
                sound.stop()
        else:
            if not self.user_score:
                self.user_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.user.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.user_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)


class OpenQuestions(LoadFiles,ScreenMixin):

    def __init__(self,user):
        super().__init__("D:/Python project/openquestions.json")
        self._load_questions()
        ScreenMixin.__init__(self)
        self.user = user
        self.continue_button = Button(screen_width//2-420,screen_height//2-60,200,50,"Continue",lambda : self.generate_fifth_round())
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.user_score=None
        self.generated_questions=0
    
    def generate_fifth_round(self):
        return HardQuestions(self.user)

    @staticmethod
    def is_correct(answer,correct_answers):
        is_correct_answer=False
        if isinstance(correct_answers,list):
            for correct_answer in correct_answers:
                is_correct_answer = answer.lower() == correct_answer.lower()
                if is_correct_answer:
                    return True
            return False
        return answer.lower() == correct_answers.lower()
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=choose_random_question(self.loaded_data)
                correct_answers = random_question["answers"]
                needed_answers=random_question['needed_answers']
                correct_answered=0
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answers])}",lambda : None))
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2+185,screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answers])}",lambda : None))
                question_text = Button(screen_width // 2-230, screen_height // 2-100,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,ImageRound.is_correct,correct_answers)
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 20000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                text=''
                self.generated_questions+=1
                click_skip=False
                print(self.generated_questions)
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if skip_button.rect.collidepoint(event.pos):
                                    click_skip=True
                                    break
                        found_answer=type_area.handle_event(event)
                    if not pygame.get_init():
                        return
                    if click_skip:
                        break
                    dt = clock.tick(60)  # Adjust the argument based on your desired frame rate
                    elapsed_time += dt

                    # Calculate remaining time
                    remaining_time = max(timer_duration - elapsed_time, 0)

                    # Convert remaining time to seconds
                    remaining_seconds = remaining_time // 1000
                    if remaining_seconds<=0:
                        break
                    self.screen.blit(self.background, (0, 0))
                    question_text.draw(self.screen)
                    type_area.draw(self.screen)
                    skip_button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        correct_answered+=1
                        found_answer = None
                        if correct_answered == needed_answers:
                            self.user.correct_answer(3)
                            print(self.user.points)
                            break
        else:
            if not self.user_score:
                self.user_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.user.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.user_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)

class HardQuestions(LoadFiles,ScreenMixin):

    def __init__(self,user):
        from MainMenu import MainMenu
        super().__init__("D:/Python project/hardquestions.json")
        self._load_questions()
        ScreenMixin.__init__(self)
        self.user = user
        self.continue_button = Button(screen_width//2-420,screen_height//2-60,200,50,"Go to main menu",lambda : MainMenu(User.User()))
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
        self.user_score=None
        self.answers=[]
        self.generated_questions=0
    
    @staticmethod
    def is_correct(answer,correct_answers):
        is_correct_answer=False
        if isinstance(correct_answers,list):
            for correct_answer in correct_answers:
                is_correct_answer = answer.lower() == correct_answer.lower()
                if is_correct_answer:
                    return True
            return False
        return answer.lower() == correct_answers.lower()
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<5:
                random_question=choose_random_question(self.loaded_data)
                correct_answers = random_question["answer"]
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(screen_width//2-175,screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answers])}",lambda : None))
                question_text = Button(screen_width // 2-230, screen_height // 2-175,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,ImageRound.is_correct,correct_answers)
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 20000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                text=''
                self.generated_questions+=1
                click_skip=False
                print(self.generated_questions)
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if skip_button.rect.collidepoint(event.pos):
                                    click_skip=True
                                    break
                        found_answer=type_area.handle_event(event)
                    if not pygame.get_init():
                        return
                    if click_skip:
                        break
                    dt = clock.tick(60)  # Adjust the argument based on your desired frame rate
                    elapsed_time += dt

                    # Calculate remaining time
                    remaining_time = max(timer_duration - elapsed_time, 0)

                    # Convert remaining time to seconds
                    remaining_seconds = remaining_time // 1000
                    if remaining_seconds<=0:
                        break
                    self.screen.blit(self.background, (0, 0))
                    question_text.draw(self.screen)
                 #   type_area.text=text
                    type_area.draw(self.screen)
                    skip_button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(5)
                        print(self.user.points)
                        break
        else:
            if not self.user_score:
                self.user_score =  Button(screen_width//2-420,screen_height//2-120,200,50,f"Your score: {self.user.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.user_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)