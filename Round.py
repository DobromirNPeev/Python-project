from typing import override
from Button import Button
import pygame
from User import User
from Constants import screen_height,screen_width,WHITE,SKIPPED,TERMINATED,VALID
from LoadFiles import LoadFiles
from RoundBase import Round
from TimeCountdown import TimeCountdown

class FirstRound(Round):

    def __init__(self,user):
        super().__init__("D:/Python project/firstround.json",user,lambda : ImageRound(user))
    
    @override
    def _create_interface(self, random_question):
          self.question_text = Button(screen_width//2-250,screen_height//2-150,750,50,random_question['question'],lambda: None)
          choices_A = Button(screen_width//2-350,screen_height//2-75,450,50,f"A) {random_question['choices'][0]}",lambda: self._is_correct(random_question['choices'][0],random_question["correct_answer"]))
          choices_B = Button(screen_width//2+125,screen_height//2-75,450,50,f"B) {random_question['choices'][1]}",lambda: self._is_correct(random_question['choices'][1],random_question["correct_answer"]))
          choices_C = Button(screen_width//2-350,screen_height//2,450,50,f"C) {random_question['choices'][2]}",lambda: self._is_correct(random_question['choices'][2],random_question["correct_answer"]))
          choices_D = Button(screen_width//2+125,screen_height//2,450,50,f"D) {random_question['choices'][3]}",lambda: self._is_correct(random_question['choices'][3],random_question["correct_answer"]))
          self.skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
          self.objects=[choices_A,choices_B,choices_C,choices_D,self.skip_button,self.question_text]
          self.found_answer = None
          self.generated_questions+=1
    
    @override
    def _check_for_correct_answer(self, points):
        if Round._check_for_correct_answer(self,points) or self.found_answer is False:
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

    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=self._choose_random_question(self.loaded_data)
                correct_answer = random_question["correct_answer"]   
                self._save_answer(correct_answer)
                self._create_interface(random_question)
                self.timer=TimeCountdown(10000,screen)
                print(self.generated_questions)
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

                    if self._check_for_correct_answer(1):
                        break
        else:
            self._render_intermediate_screen(screen)


class ImageRound(Round):
    
    def __init__(self,user):
        super().__init__('D:/Python project/images/questionsforimages.json',user,lambda: AudioRound(user))
        self.image_data=LoadFiles.load_images(self.loaded_data,"D:/Python project/images")

    @override
    def _render_interface(self,screen):
        Round._render_interface(self,screen)
        screen.blit(self.random_question['image'],self.random_question['rect'])
    
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

                    if self._check_for_correct_answer(2):
                        break
        else:
            self._render_intermediate_screen(screen)

class AudioRound(Round):

    def __init__(self,user):
        super().__init__('D:/Python project/audio-files/audio-files.json',user,lambda : OpenQuestions(user))
        self.audio_data=LoadFiles.load_audio(self.loaded_data,"D:/Python project/audio-files")

    def _create_interface(self, random_question):
        Round._create_interface(self,random_question)
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound((random_question['audio']-20).raw_data)
        self.sound.play()

    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=self._choose_random_question(self.audio_data)
                correct_answer = random_question["answers"]
                self._save_answer(correct_answer)
                self._create_interface(random_question)
                self.timer=TimeCountdown(10000,screen)
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

                    if self._check_for_correct_answer(3):
                        break
                self.sound.stop()
        else:
            self._render_intermediate_screen(screen)


class OpenQuestions(Round):

    def __init__(self,user):
        super().__init__("D:/Python project/openquestions.json",user,lambda : HardQuestions(user))
    
    @override
    def _check_for_correct_answer(self, points):
        if self.found_answer is True:
            self.correct_answered+=1
            self.found_answer = None
            if self.correct_answered == self.needed_answers:
                self.user.correct_answer(points)
                print(self.user.points)
                return True

    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<10:
                random_question=self._choose_random_question(self.loaded_data)
                correct_answers = random_question["answers"]
                self.needed_answers=random_question['needed_answers']
                self.correct_answered=0
                self._save_answer(correct_answers)
                self._create_interface(random_question)
                self.timer=TimeCountdown(10000,screen)
                print(self.generated_questions)
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

                    if self._check_for_correct_answer(3):
                        break
        else:
            self._render_intermediate_screen(screen)

class HardQuestions(Round):

    def __init__(self,user):
        from MainMenu import MainMenu
        super().__init__("D:/Python project/hardquestions.json",user,lambda : MainMenu(User()))
    
    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<5:
                random_question=self._choose_random_question(self.loaded_data)
                correct_answers = random_question["answers"]
                self._save_answer(correct_answers)
                self._create_interface(random_question)
                self.timer = TimeCountdown(10000,screen)
                print(self.generated_questions)
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

                    if self._check_for_correct_answer(5):
                        break
        else:
            self._render_intermediate_screen(screen)