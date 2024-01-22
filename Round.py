from Button import Button
import pygame
import json
import random
import copy
import os

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
        self.copy_questions=copy.deepcopy(self.loaded_data)
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
            for self.generated_questions in range(0,10):
                random_question=self.choose_random_question(self.loaded_data)
                correct_answer = random_question["correct_answer"]
                question_text = Button(self.midPoint[0]-250,self.midPoint[1]-150,750,50,random_question['question'],lambda: None)
                choices_A = Button(self.midPoint[0]-350,self.midPoint[1]-75,450,50,f"A) {random_question['choices'][0]}",lambda: self.is_correct(random_question['choices'][0],correct_answer))
                choices_B = Button(self.midPoint[0]+125,self.midPoint[1]-75,450,50,f"B) {random_question['choices'][1]}",lambda: self.is_correct(random_question['choices'][1],correct_answer))
                choices_C = Button(self.midPoint[0]-350,self.midPoint[1],450,50,f"C) {random_question['choices'][2]}",lambda: self.is_correct(random_question['choices'][2],correct_answer))
                choices_D = Button(self.midPoint[0]+125,self.midPoint[1],450,50,f"D) {random_question['choices'][3]}",lambda: self.is_correct(random_question['choices'][3],correct_answer))
                choices_buttons=[choices_A,choices_B,choices_C,choices_D]
                clock = pygame.time.Clock()
                timer_duration = 5000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                print(self.generated_questions)
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                            for button in choices_buttons:
                                if button.rect.collidepoint(event.pos):
                                    found_answer = button.handle_event(event)
                                    if found_answer is not None:
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
                    choices_A.draw(self.screen)
                    choices_B.draw(self.screen)
                    choices_C.draw(self.screen)
                    choices_D.draw(self.screen)
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
        midPoint=getMidPoint(0,0,800,600)
       # self.copy_questions=copy.deepcopy(self.image_data)
        self.continue_button = Button(midPoint[0],midPoint[1]-50,200,50,"Continue",lambda : self.generate_second_round())
        self.user = user
        self.generated_questions=0
    
    def load_images_from_folder(self,image_folder,json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

        self.image_data = []
        for entry in data['questions']:
            question = entry['question']
            image_filename = entry['image']
            correct_answer = entry['correct_answer']

            img_path = os.path.join(image_folder, image_filename)
            img = pygame.image.load(img_path)

            self.image_data.append( {'question' : entry['question'], 'image': img, 'rect': img.get_rect(center=(self.screen_width // 2, self.screen_height // 2-150)), 'correct_answer': correct_answer})

    @staticmethod
    def is_correct(answer,correct_answer):
        return answer.lower() == correct_answer.lower()

    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
            for self.generated_questions in range(0,10):
                random_question=Round.choose_random_question(self.image_data)
                correct_answer = random_question["correct_answer"]
                question_text = Button(self.screen_width // 2-222, self.screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = Button(self.screen_width // 2-115, self.screen_height // 2+84,250,35,"",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 1000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                text=''
                print(self.generated_questions)
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                # Handle Enter key (you can add more logic here)
                                found_answer=self.is_correct(text,correct_answer)
                                text = ""
                            elif event.key == pygame.K_BACKSPACE:
                                # Handle Backspace key
                                text = text[:-1]
                            else:
                                # Handle other key presses
                                text += event.unicode
                        
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
                        self.user.correct_answer(1)
                        print(self.user.points)
                        break
            else:
                self.screen.blit(self.background, (0, 0))
                self.continue_button.draw(self.screen)

class AudioRound:

    def __init__(self,user):
        self.screen_width, self.screen_height = 1000, 600
        self.load_audio_from_folder("D:/Python project/audio-files","D:/Python project/images/questionsforimages.json")
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.screen=pygame.display.set_mode((self.screen_width, self.screen_height))
        midPoint=getMidPoint(0,0,800,600)
       # self.copy_questions=copy.deepcopy(self.image_data)
        self.continue_button = Button(midPoint[0],midPoint[1]-50,200,50,"Continue",lambda : self.generate_second_round())
        self.user = user
        self.generated_questions=0

    def load_audio_from_folder(self,image_folder,json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

        self.image_data = []
        for entry in data['questions']:
            question = entry['question']
            image_filename = entry['image']
            correct_answer = entry['correct_answer']

            img_path = os.path.join(image_folder, image_filename)
            img = pygame.image.load(img_path)

            self.image_data.append( {'question' : entry['question'], 'image': img, 'rect': img.get_rect(center=(self.screen_width // 2, self.screen_height // 2-150)), 'correct_answer': correct_answer})