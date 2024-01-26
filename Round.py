from Button import Button
import pygame
import json
import random
import copy
import os
import pydub

WHITE = (255, 255, 255)


def getMidPoint(x,y,x1,y1):
        return [(x + x1) / 2.0,(y + y1) / 2.0]

class Round:
    def __init__(self, questions):
        with open(questions, 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)
            
    @staticmethod
    def choose_random_question(questions):
        if not questions:
            return None

        random_index = random.randrange(len(questions))
        return questions.pop(random_index)

class FirstRound(Round):

    def __init__(self,user):
        super().__init__("D:/Python project/firstround.json")
        self.font = pygame.font.Font(None, 36)
        self.screen_width, self.screen_height = 1000, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.screen=pygame.display.set_mode((self.screen_width, self.screen_height))
        self.midPoint=getMidPoint(0,0,800,600)
        self.user = user
        midPoint=getMidPoint(0,0,800,600)
        self.continue_button = Button(midPoint[0],midPoint[1]-50,200,50,"Continue",lambda : self.generate_second_round())
        self.buttons=[self.continue_button]
        self.generated_questions=0

    def generate_second_round(self):
        return ImageRound(self.user)

    @staticmethod
    def is_correct(answer,correct_answer):
        return answer==correct_answer

    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
                random_question=self.choose_random_question(self.loaded_data)
                correct_answer = random_question["correct_answer"]
                question_text = Button(self.midPoint[0]-250,self.midPoint[1]-150,750,50,random_question['question'],lambda: None)
                choices_A = Button(self.midPoint[0]-350,self.midPoint[1]-75,450,50,f"A) {random_question['choices'][0]}",lambda: self.is_correct(random_question['choices'][0],correct_answer))
                choices_B = Button(self.midPoint[0]+125,self.midPoint[1]-75,450,50,f"B) {random_question['choices'][1]}",lambda: self.is_correct(random_question['choices'][1],correct_answer))
                choices_C = Button(self.midPoint[0]-350,self.midPoint[1],450,50,f"C) {random_question['choices'][2]}",lambda: self.is_correct(random_question['choices'][2],correct_answer))
                choices_D = Button(self.midPoint[0]+125,self.midPoint[1],450,50,f"D) {random_question['choices'][3]}",lambda: self.is_correct(random_question['choices'][3],correct_answer))
                skip_button= Button(self.screen_width//2-65,self.midPoint[1]+125,150,50,f"Skip",lambda: None)
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
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(1)
                        print(self.user.points)
                        break
                    elif found_answer is False:
                        break
        else:
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)


class ImageRound:
    
    def __init__(self,user):
        self.screen_width, self.screen_height = 1000, 600
        self.load_images_from_folder("D:/Python project/images","D:/Python project/images/questionsforimages.json")
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.screen=pygame.display.set_mode((self.screen_width, self.screen_height))
        self.midPoint=getMidPoint(0,0,800,600)
       # self.copy_questions=copy.deepcopy(self.image_data)
        self.continue_button = Button(self.midPoint[0],self.midPoint[1]-50,200,50,"Continue",lambda : self.generate_thrid_round())
        self.buttons=[self.continue_button]
        self.user = user
        self.generated_questions=0
    
    def generate_thrid_round(self):
        return AudioRound(self.user)

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

    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
            for self.generated_questions in range(0,10):
                random_question=Round.choose_random_question(self.image_data)
                correct_answer = random_question["correct_answer"]
                question_text = Button(self.screen_width // 2-222, self.screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = Button(self.screen_width // 2-115, self.screen_height // 2+84,250,35,"",lambda: None)
                skip_button= Button(self.screen_width//2-65,self.midPoint[1]+125,150,50,f"Skip",lambda: None)
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
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                found_answer=self.is_correct(text,correct_answer)
                                text = ""
                            elif event.key == pygame.K_BACKSPACE:
                                # Handle Backspace key
                                text = text[:-1]
                            else:
                                # Handle other key presses
                                text += event.unicode
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
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    text_surface = font.render(text, True, (0,0,0))
                    text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2+100))
                    screen.blit(text_surface, text_rect)
                    cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
                    pygame.draw.rect(screen, (0,0,0), cursor_rect)
                    screen.blit(random_question['image'],random_question['rect'])
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(2)
                        print(self.user.points)
                        break
        else:
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)

class AudioRound:

    def __init__(self,user):
        self.screen_width, self.screen_height = 1000, 600
        self.load_audio_from_folder("D:/Python project/audio-files","D:/Python project/audio-files/audio-files.json")
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.screen=pygame.display.set_mode((self.screen_width, self.screen_height))
        midPoint=getMidPoint(0,0,800,600)
       # self.copy_questions=copy.deepcopy(self.image_data)
        self.continue_button = Button(midPoint[0],midPoint[1]-50,200,50,"Continue",lambda : self.generate_fourth_round())
        self.buttons=[self.continue_button]
        self.user = user
        self.generated_questions=0

    def generate_fourth_round(self):
        return OpenQuestions(self.user)

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

    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
            for self.generated_questions in range(0,10):
                random_question=Round.choose_random_question(self.audio_data)
                correct_answer = random_question["correct_answer"]
                question_text = Button(self.screen_width // 2-222, self.screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = Button(self.screen_width // 2-115, self.screen_height // 2+84,250,35,"",lambda: None)
                skip_button= Button(self.screen_width//2-65,self.screen_height//2+125,150,50,f"Skip",lambda: None)
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
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                # Handle Enter key (you can add more logic here)
                                found_answer=ImageRound.is_correct(text,correct_answer)
                                text = ""
                            elif event.key == pygame.K_BACKSPACE:
                                # Handle Backspace key
                                text = text[:-1]
                            else:
                                # Handle other key presses
                                text += event.unicode
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
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    text_surface = font.render(text, True, (0,0,0))
                    text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2+100))
                    screen.blit(text_surface, text_rect)
                    cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
                    pygame.draw.rect(screen, (0,0,0), cursor_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(3)
                        print(self.user.points)
                        break
                sound.stop()
        else:
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)

class OpenQuestions(Round):

    def __init__(self,user):
        super().__init__("D:/Python project/openquestions.json")
        self.font = pygame.font.Font(None, 36)
        self.screen_width, self.screen_height = 1000, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.screen=pygame.display.set_mode((self.screen_width, self.screen_height))
        self.midPoint=getMidPoint(0,0,800,600)
        self.user = user
        midPoint=getMidPoint(0,0,800,600)
        self.continue_button = Button(midPoint[0],midPoint[1]-50,200,50,"Continue",lambda : self.generate_fifth_round())
        self.buttons=[self.continue_button]
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

    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
                random_question=Round.choose_random_question(self.loaded_data)
                correct_answers = random_question["answers"]
                needed_answers=random_question['needed_answers']
                correct_answered=0
                question_text = Button(self.screen_width // 2-230, self.screen_height // 2-100,500,50,random_question['question'],lambda: None)
                type_area = Button(self.screen_width // 2-145, self.screen_height // 2+84,325,35,"",lambda: None)
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
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                found_answer=self.is_correct(text,correct_answers)
                                text=''
                            elif event.key == pygame.K_BACKSPACE:
                                    text = text[:-1]
                            else:
                                # Handle other key presses
                                text += event.unicode
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
                    type_area.text=text
                    type_area.draw(self.screen)
                    skip_button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                  #  text_surface = font.render(type_area.text, True, (0,0,0))
                  #  text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2+100))
                   # screen.blit(text_surface, text_rect)
                   # cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
                  #  pygame.draw.rect(screen, (0,0,0), cursor_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        correct_answered+=1
                        found_answer = None
                        if correct_answered == needed_answers:
                            self.user.correct_answer(3)
                            print(self.user.points)
                            break
        else:
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)

class HardQuestions(Round):
    def __init__(self,user):
        super().__init__("D:/Python project/hardquestions.json")
        self.font = pygame.font.Font(None, 36)
        self.screen_width, self.screen_height = 1000, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.screen=pygame.display.set_mode((self.screen_width, self.screen_height))
        self.midPoint=getMidPoint(0,0,800,600)
        self.user = user
        midPoint=getMidPoint(0,0,800,600)
        self.continue_button = Button(midPoint[0],midPoint[1]-50,200,50,"Continue",lambda : None)
        self.buttons=[self.continue_button]
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

    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
                random_question=Round.choose_random_question(self.loaded_data)
                correct_answers = random_question["answer"]
                question_text = Button(self.screen_width // 2-230, self.screen_height // 2-100,500,50,random_question['question'],lambda: None)
                type_area = Button(self.screen_width // 2-145, self.screen_height // 2+84,325,35,"",lambda: None)
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
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                found_answer=self.is_correct(text,correct_answers)
                                text=''
                            elif event.key == pygame.K_BACKSPACE:
                                    text = text[:-1]
                            else:
                                # Handle other key presses
                                text += event.unicode
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
                    type_area.text=text
                    type_area.draw(self.screen)
                    skip_button.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                  #  text_surface = font.render(type_area.text, True, (0,0,0))
                  #  text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2+100))
                   # screen.blit(text_surface, text_rect)
                   # cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
                  #  pygame.draw.rect(screen, (0,0,0), cursor_rect)
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(5)
                        print(self.user.points)
                        break
        else:
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)