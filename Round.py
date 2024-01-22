from Button import Button
import pygame
import json
import random
import copy


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
    def __init__(self):
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

    def render(self,screen):
        for i in range(0,10):
            random_question=self.choose_random_question(self.loaded_data)
            
            question_text = Button(self.midPoint[0],self.midPoint[1]-50,2000,50,random_question['question'],lambda: None)
            choices_text = ''.join([f"{j + 1}. {choice}" for j, choice in enumerate(random_question['choices'])])
            text = f"{question_text}\n\n{choices_text}"

            clock = pygame.time.Clock()
            timer_duration = 5000 
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
                question_text.draw(self.screen)
                pygame.display.flip()