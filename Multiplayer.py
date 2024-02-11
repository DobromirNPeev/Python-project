from typing import override
import pygame
from Button import Button
from textbox import TextBoxForMultiplayer,TextBoxForQuestions
from User import User
import json
import random
import os
import pydub
from ScreenMixin import ScreenMixin
from Round import LoadFiles

WHITE = (255, 255, 255)

def getMidPoint(x,y,x1,y1):
        return [(x + x1) / 2.0,(y + y1) / 2.0]

def choose_random_question(questions):
        if not questions:
            return None

        random_index = random.randrange(len(questions))
        return questions.pop(random_index)

class PreScreenMutliplayer(ScreenMixin):

    def __init__(self):
        super().__init__()
        self.user1=User()
        self.user2=User()
        self.enter_player1_name=Button(self.screen_width//2-100,self.screen_height//2-150,300,50,"Player 1 enter name:",lambda: None)
        self.enter_player1_textbox=TextBoxForMultiplayer(self.screen_width // 2-100, self.screen_height // 2-90,250,35,self.user1)
        self.enter_player2_name=Button(self.screen_width//2-100,self.screen_height//2-40,300,50,"Player 2 enter name:",lambda: None)
        self.enter_player2_textbox=TextBoxForMultiplayer(self.screen_width // 2-100, self.screen_height // 2+20,250,35,self.user2)
        self.ready=Button(self.screen_width//2-100,self.screen_height//2+80,200,50,"Ready",lambda: self.start_game())
        self.buttons=[self.enter_player1_name,self.enter_player1_textbox,self.enter_player2_name,self.enter_player2_textbox,self.ready]

    def start_game(self):
        clock = pygame.time.Clock()
        timer_duration = 1000 
        elapsed_time = 0 
        font = pygame.font.Font(None, 36)
        while True:
            dt = clock.tick(60)  # Adjust the argument based on your desired frame rate
            elapsed_time += dt

            # Calculate remaining time
            remaining_time = max(timer_duration - elapsed_time, 0)

            # Convert remaining time to seconds
            remaining_seconds = remaining_time // 1000
            if remaining_seconds<=0:
                break
            self.screen.blit(self.background, (0, 0))
            timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, (255, 255, 255))
            timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(timer_text, timer_rect)
            pygame.display.flip()
        return FirstRoundMultiplayer(self.user1,self.user2)
    
    @override
    def render(self,screen):
        self.screen.fill(WHITE)
        screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(screen)     

class FirstRoundMultiplayer(LoadFiles,ScreenMixin):

    def __init__(self,player1,player2):
        super().__init__("D:/Python project/firstround.json")
        self.load_questions()
        ScreenMixin.__init__(self)
        self.midPoint=getMidPoint(0,0,800,600)
        self.player1 = player1
        self.player2 = player2
        self.current_player=None
        self.continue_button = Button(self.screen_width//2-420,self.screen_height//2-60,200,50,"Continue",lambda : ImageRoundMultiplayer(self.player1,self.player2))
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.player1_score = None
        self.player2_score=None
        self.buttons=[self.continue_button]
        self.generated_questions=0

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
                    self.answers.append(Button(self.screen_width//2-175,self.screen_height//2-self.offset,200,50,f"{self.generated_questions+1}) {correct_answer}",lambda : None))
                    self.current_player=self.player1
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2+180,self.screen_height//2-self.offset_upper_half,200,50,f"{self.generated_questions+1}) {correct_answer}",lambda : None))
                    self.current_player=self.player2
                player_turn=Button(self.screen_width//2-100,self.screen_height//2-210,300,50,f"{self.current_player.name}'s turn",lambda: None)
                question_text = Button(self.midPoint[0]-250,self.midPoint[1]-150,750,50,random_question['question'],lambda: None)
                choices_A = Button(self.midPoint[0]-350,self.midPoint[1]-75,450,50,f"A) {random_question['choices'][0]}",lambda: self.is_correct(random_question['choices'][0],correct_answer))
                choices_B = Button(self.midPoint[0]+125,self.midPoint[1]-75,450,50,f"B) {random_question['choices'][1]}",lambda: self.is_correct(random_question['choices'][1],correct_answer))
                choices_C = Button(self.midPoint[0]-350,self.midPoint[1],450,50,f"C) {random_question['choices'][2]}",lambda: self.is_correct(random_question['choices'][2],correct_answer))
                choices_D = Button(self.midPoint[0]+125,self.midPoint[1],450,50,f"D) {random_question['choices'][3]}",lambda: self.is_correct(random_question['choices'][3],correct_answer))
                skip_button= Button(self.screen_width//2-65,self.midPoint[1]+125,150,50,f"Skip",lambda: None)
                choices_buttons=[choices_A,choices_B,choices_C,choices_D,skip_button]
                clock = pygame.time.Clock()
                timer_duration = 1000 
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
                    player_turn.draw(self.screen)
                    for button in choices_buttons:
                        button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.current_player.correct_answer(1)
                        print(self.current_player.points)
                        break
                    elif found_answer is False:
                        break
        else:
            if not self.player1_score and not self.player2_score:
                self.player1_score =  Button(self.screen_width//2-420,self.screen_height//2-240,200,50,f"{self.player1.name}'s score: {self.player1.points}",lambda : None)
                self.player2_score =  Button(self.screen_width//2-420,self.screen_height//2-150,200,50,f"{self.player2.name}'s score: {self.player2.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.player1_score.draw(self.screen)
            self.player2_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)

class ImageRoundMultiplayer(ScreenMixin):
    
    def __init__(self,player1,player2):
        super().__init__()
        self.load_images_from_folder("D:/Python project/images","D:/Python project/images/questionsforimages.json")
        self.midPoint=getMidPoint(0,0,800,600)
       # self.copy_questions=copy.deepcopy(self.image_data)
        self.continue_button = Button(self.screen_width//2-420,self.screen_height//2-60,200,50,"Continue",lambda : AudioRoundMultiplayer(self.player1,self.player2))
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.player1 = player1
        self.player2 = player2
        self.player1_score = None
        self.player2_score=None
        self.generated_questions=0
    

    def load_images_from_folder(self,image_folder,json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

        self.image_data = []
        for entry in data['questions']:
            question = entry['question']
            image_filename = entry['image']
            correct_answers = entry['correct_answer']

            img_path = os.path.join(image_folder, image_filename)
            img = pygame.image.load(img_path)

            self.image_data.append( {'question' : entry['question'], 'image': img, 'rect': img.get_rect(center=(self.screen_width // 2, self.screen_height // 2-150)), 'correct_answer': correct_answers})

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
                correct_answer = random_question["correct_answer"]
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2-175,self.screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                    self.current_player=self.player1
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2+185,self.screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                    self.current_player=self.player2
                player_turn=Button(self.screen_width//2-115,self.screen_height//2+225,250,50,f"{self.current_player.name}'s turn",lambda: None)
                question_text = Button(self.screen_width // 2-222, self.screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(self.screen_width // 2-115, self.screen_height // 2+84,250,35,self.is_correct,correct_answer)
                skip_button= Button(self.screen_width//2-65,self.midPoint[1]+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 1000 
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
                    player_turn.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    screen.blit(random_question['image'],random_question['rect'])
                    pygame.display.flip()

                    if found_answer is True:
                        self.current_player.correct_answer(2)
                        print(self.current_player.points)
                        break
        else:
            if not self.player1_score and not self.player2_score:
                self.player1_score =  Button(self.screen_width//2-420,self.screen_height//2-240,200,50,f"{self.player1.name}'s score: {self.player1.points}",lambda : None)
                self.player2_score =  Button(self.screen_width//2-420,self.screen_height//2-150,200,50,f"{self.player2.name}'s score: {self.player2.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.player1_score.draw(self.screen)
            self.player2_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)

class AudioRoundMultiplayer(ScreenMixin):

    def __init__(self,player1,player2):
        super().__init__()
        self.load_audio_from_folder("D:/Python project/audio-files","D:/Python project/audio-files/audio-files.json")
        self.continue_button = Button(self.screen_width//2-420,self.screen_height//2-60,200,50,"Continue",lambda : OpenQuestionsMultiplayer(self.player1,self.player2))
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.player1 = player1
        self.player2 = player2
        self.player1_score = None
        self.player2_score=None
        self.generated_questions=0


    def load_audio_from_folder(self,audio_folder,json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

        self.audio_data = []
        for entry in data['audio_files']:
            question = entry['question']
            audio_filename = entry['file_path']
            answer = entry['answer']

            audio_path = os.path.join(audio_folder, audio_filename)
            audio = pydub.AudioSegment.from_file(audio_path)

            self.audio_data.append( {'question' : entry['question'],'audio':audio , 'correct_answer': answer})

    @override
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
            for self.generated_questions in range(0,10):
                random_question=choose_random_question(self.audio_data)
                correct_answer = random_question["correct_answer"]
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2-175,self.screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                    self.current_player=self.player1
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2+185,self.screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answer])}",lambda : None))
                    self.current_player=self.player2
                player_turn=Button(self.screen_width//2-115,self.screen_height//2+225,250,50,f"{self.current_player.name}'s turn",lambda: None)
                question_text = Button(self.screen_width // 2-222, self.screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(self.screen_width // 2-115, self.screen_height // 2+84,250,35,ImageRoundMultiplayer.is_correct,correct_answer)
                skip_button= Button(self.screen_width//2-65,self.screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 1000 
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
                    player_turn.draw(self.screen)
                    type_area.draw(self.screen)
                    skip_button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.current_player.correct_answer(3)
                        print(self.current_player.points)
                        break
                sound.stop()
        else:
            if not self.player1_score and not self.player2_score:
                self.player1_score =  Button(self.screen_width//2-420,self.screen_height//2-240,200,50,f"{self.player1.name}'s score: {self.player1.points}",lambda : None)
                self.player2_score =  Button(self.screen_width//2-420,self.screen_height//2-150,200,50,f"{self.player2.name}'s score: {self.player2.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.player1_score.draw(self.screen)
            self.player2_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)


class OpenQuestionsMultiplayer(LoadFiles,ScreenMixin):

    def __init__(self,player1,player2):
        super().__init__("D:/Python project/openquestions.json")
        self.load_questions()
        ScreenMixin.__init__(self)
        self.midPoint=getMidPoint(0,0,800,600)
        self.player1 = player1
        self.player2 = player2
        self.player1_score = None
        self.player2_score=None
        self.continue_button = Button(self.screen_width//2-420,self.screen_height//2-60,200,50,"Continue",lambda : HardQuestionsMultiplayer(self.player1,self.player2))
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
        self.answers=[]
        self.user_score=None
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
        if self.generated_questions<10:
                random_question=choose_random_question(self.loaded_data)
                correct_answers = random_question["answers"]
                needed_answers=random_question['needed_answers']
                correct_answered=0
                if self.generated_questions<5:
                    if len(self.answers)%5!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2-175,self.screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answers])}",lambda : None))
                    self.current_player=self.player1
                else:
                    if len(self.answers)%5!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2+185,self.screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answers])}",lambda : None))
                    self.current_player=self.player2
                player_turn=Button(self.screen_width//2-115,self.screen_height//2+225,250,50,f"{self.current_player.name}'s turn",lambda: None)
                question_text = Button(self.screen_width // 2-230, self.screen_height // 2-100,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(self.screen_width // 2-115, self.screen_height // 2+84,250,35,ImageRoundMultiplayer.is_correct,correct_answers)
                skip_button= Button(self.screen_width//2-65,self.screen_height//2+125,150,50,f"Skip",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 1000 
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
                    player_turn.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        correct_answered+=1
                        found_answer = None
                        if correct_answered == needed_answers:
                            self.current_player.correct_answer(3)
                            print(self.current_player.points)
                            break
        else:
            if not self.player1_score and not self.player2_score:
                self.player1_score =  Button(self.screen_width//2-420,self.screen_height//2-240,200,50,f"{self.player1.name}'s score: {self.player1.points}",lambda : None)
                self.player2_score =  Button(self.screen_width//2-420,self.screen_height//2-150,200,50,f"{self.player2.name}'s score: {self.player2.points}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.player1_score.draw(self.screen)
            self.player2_score.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)

class HardQuestionsMultiplayer(LoadFiles,ScreenMixin):
    def __init__(self,player1,player2):
        from MainMenu import MainMenu
        super().__init__("D:/Python project/hardquestions.json")
        self.load_questions()
        ScreenMixin.__init__(self)
        self.midPoint=getMidPoint(0,0,800,600)
        self.player1 = player1
        self.player2 = player2
        self.player1_score = None
        self.player2_score=None
        midPoint=getMidPoint(0,0,800,600)
        self.continue_button = Button(self.screen_width//2-420,self.screen_height//2-60,200,50,"Go to main menu",lambda : MainMenu(User()))
        self.buttons=[self.continue_button]
        self.offset=260
        self.offset_upper_half=260
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
        if self.generated_questions<6:
                random_question=choose_random_question(self.loaded_data)
                correct_answers = random_question["answer"]
                if self.generated_questions<3:
                    if len(self.answers)%3!=0:
                        self.offset-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2-175,self.screen_height//2-self.offset,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answers])}",lambda : None))
                    self.current_player=self.player1
                else:
                    if len(self.answers)%3!=0:
                        self.offset_upper_half-=self.answers[-1].rect.height+15
                    self.answers.append(Button(self.screen_width//2+185,self.screen_height//2-self.offset_upper_half,300,50,f"{self.generated_questions+1}) {', '.join([str(element) for element in correct_answers])}",lambda : None))
                    self.current_player=self.player2
                player_turn=Button(self.screen_width//2-115,self.screen_height//2+225,250,50,f"{self.current_player.name}'s turn",lambda: None)
                question_text = Button(self.screen_width // 2-230, self.screen_height // 2-175,500,50,random_question['question'],lambda: None)
                type_area = TextBoxForQuestions(self.screen_width // 2-115, self.screen_height // 2+84,250,35,ImageRoundMultiplayer.is_correct,correct_answers)
                skip_button= Button(self.screen_width//2-65,self.screen_height//2+125,150,50,f"Skip",lambda: None)
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
                    player_turn.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.current_player.correct_answer(5)
                        print(self.current_player.points)
                        break
        else:
            if not self.player1_score and not self.player2_score:
                self.player1_score =  Button(self.screen_width//2-420,self.screen_height//2-240,200,50,f"{self.player1.name}'s score: {self.player1.points}",lambda : None)
                self.player2_score =  Button(self.screen_width//2-420,self.screen_height//2-150,200,50,f"{self.player2.name}'s score: {self.player2.points}",lambda : None)
                self.winner= self.player1 if self.player1.points>self.player2.points else self.player2
                self.winner_button=Button(self.screen_width//2-100,self.screen_height//2+50,200,50,f"The winner is {self.winner.name}",lambda : None)
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)
            self.player1_score.draw(self.screen)
            self.player2_score.draw(self.screen)
            self.winner_button.draw(self.screen)
            for answer in self.answers:
                answer.draw(self.screen)
