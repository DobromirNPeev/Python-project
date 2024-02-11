from typing import override
from Button import Button
import pygame
import random
from textbox import TextBoxForQuestions
from ScreenMixin import ScreenMixin
from User import User
from Constants import screen_height,screen_width,WHITE
from LoadFiles import LoadFiles
from RoundBase import Round
from TimeCountdown import TimeCountdown

class FirstRound(LoadFiles,ScreenMixin,Round):

    def __init__(self,user):
        LoadFiles.__init__(self,"D:/Python project/firstround.json")
        self._load_questions()
        ScreenMixin.__init__(self)
        Round.__init__(self,user,lambda : ImageRound(user))
    
    @override
    def _is_correct(self,answer,correct_answer):
        return answer==correct_answer
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=self._choose_random_question(self.loaded_data)
                correct_answer = random_question["correct_answer"]   
                self._save_answer(correct_answer)
                question_text = Button(screen_width//2-250,screen_height//2-150,750,50,random_question['question'],lambda: None)
                choices_A = Button(screen_width//2-350,screen_height//2-75,450,50,f"A) {random_question['choices'][0]}",lambda: self._is_correct(random_question['choices'][0],correct_answer))
                choices_B = Button(screen_width//2+125,screen_height//2-75,450,50,f"B) {random_question['choices'][1]}",lambda: self._is_correct(random_question['choices'][1],correct_answer))
                choices_C = Button(screen_width//2-350,screen_height//2,450,50,f"C) {random_question['choices'][2]}",lambda: self._is_correct(random_question['choices'][2],correct_answer))
                choices_D = Button(screen_width//2+125,screen_height//2,450,50,f"D) {random_question['choices'][3]}",lambda: self._is_correct(random_question['choices'][3],correct_answer))
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                choices_buttons=[choices_A,choices_B,choices_C,choices_D,skip_button]
                clock = pygame.time.Clock()
                timer_duration = 8000 
                elapsed_time = 0 
                found_answer = None
                click_skip=False
                self.generated_questions+=1
                print(self.generated_questions)
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
                    timer_text = self.font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
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
            self._render_intermediate_screen()


class ImageRound(LoadFiles,ScreenMixin,Round):
    
    def __init__(self,user):
        LoadFiles.__init__(self,'D:/Python project/images/questionsforimages.json')
        self._load_images("D:/Python project/images")
        ScreenMixin.__init__(self)
        Round.__init__(self,user,lambda: AudioRound(user))

    @override
    def _draw_interface(self, screen, random_question):
          screen.blit(self.background, (0, 0))
          self.timer.draw_countdown()
          self.question_text.draw(screen)
          self.type_area.draw(screen)
          self.skip_button.draw(screen)
          screen.blit(random_question['image'],random_question['rect'])
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=self._choose_random_question(self.image_data)
                correct_answer = random_question["answers"]
                self._save_answer(correct_answer)
                self._create_interface(random_question)
                self.timer=TimeCountdown(10000,screen)
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.skip_button.rect.collidepoint(event.pos):
                                    self.click_skip=True
                                    break
                        found_answer=self.type_area.handle_event(event)
                    if not pygame.get_init():
                        return
                    if self.click_skip:
                        break
                    self.timer.tick()
                    if not self.timer:
                        break
                    self._draw_interface(screen)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(2)
                        print(self.user.points)
                        break
        else:
            self._render_intermediate_screen()

class AudioRound(LoadFiles,ScreenMixin,Round):

    def __init__(self,user):
        LoadFiles.__init__(self,'D:/Python project/audio-files/audio-files.json')
        self._load_audio("D:/Python project/audio-files")
        ScreenMixin.__init__(self)
        Round.__init__(self,user,lambda : OpenQuestions(user))

    @override
    def _create_interface(self, random_question):
        Round._create_interface(random_question)

    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=self._choose_random_question(self.audio_data)
                audio=random_question['audio']
                print(self.generated_questions)
                pygame.mixer.init()
                sound = pygame.mixer.Sound((audio-20).raw_data)
                sound.play()
                correct_answer = random_question["answers"]
                self._save_answer(correct_answer)
                self._create_interface(random_question)
                clock = pygame.time.Clock()
                timer_duration = 8000 
                elapsed_time = 0 
                found_answer = None
                click_skip = False
                self.generated_questions+=1
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.skip_button.rect.collidepoint(event.pos):
                                        click_skip=True
                                        break
                        found_answer=self.type_area.handle_event(event)
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
                    self.question_text.draw(self.screen)
                    self.type_area.draw(self.screen)
                    self.skip_button.draw(self.screen)
                    timer_text = self.font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(3)
                        print(self.user.points)
                        break
                sound.stop()
        else:
            self._render_intermediate_screen()


class OpenQuestions(LoadFiles,ScreenMixin,Round):

    def __init__(self,user):
        LoadFiles.__init__(self,"D:/Python project/openquestions.json")
        self._load_questions()
        ScreenMixin.__init__(self)
        Round.__init__(self,user,lambda : HardQuestions(user))
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=self._choose_random_question(self.loaded_data)
                correct_answers = random_question["answers"]
                needed_answers=random_question['needed_answers']
                correct_answered=0
                self._save_answer(correct_answers)
                question_text = Button(screen_width // 2-230, screen_height // 2-100,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,correct_answers)
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 20000 
                elapsed_time = 0 
                found_answer = None
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
                    timer_text = self.font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
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
            self._render_intermediate_screen()

class HardQuestions(LoadFiles,ScreenMixin,Round):

    def __init__(self,user):
        from MainMenu import MainMenu
        LoadFiles.__init__(self,"D:/Python project/hardquestions.json")
        self._load_questions()
        ScreenMixin.__init__(self)
        Round.__init__(self,user,lambda : MainMenu(User()))
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<5:
                random_question=self._choose_random_question(self.loaded_data)
                correct_answers = random_question["answer"]
                self._save_answer(correct_answers)
                question_text = Button(screen_width // 2-230, screen_height // 2-175,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,correct_answers)
                skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 20000 
                elapsed_time = 0 
                found_answer = None
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
                    timer_text = self.font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(5)
                        print(self.user.points)
                        break
        else:
            self._render_intermediate_screen()