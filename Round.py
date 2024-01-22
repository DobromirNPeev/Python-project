from Button import Button
import pygame
import json
import random
import copy

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

    @staticmethod
    def is_correct(answer,correct_answer):
        return answer==correct_answer

    def render(self,screen):
        for i in range(0,10):
            random_question=self.choose_random_question(self.loaded_data)

            correct_answer = random_question["correct_answer"]
            question_text = Button(self.midPoint[0]-250,self.midPoint[1]-150,750,50,random_question['question'],lambda: None)
            choices_A = Button(self.midPoint[0]-350,self.midPoint[1]-75,450,50,f"A) {random_question['choices'][0]}",lambda: self.is_correct(random_question['choices'][0],correct_answer))
            choices_B = Button(self.midPoint[0]+125,self.midPoint[1]-75,450,50,f"B) {random_question['choices'][1]}",lambda: self.is_correct(random_question['choices'][1],correct_answer))
            choices_C = Button(self.midPoint[0]-350,self.midPoint[1],450,50,f"C) {random_question['choices'][2]}",lambda: self.is_correct(random_question['choices'][2],correct_answer))
            choices_D = Button(self.midPoint[0]+125,self.midPoint[1],450,50,f"D) {random_question['choices'][3]}",lambda: self.is_correct(random_question['choices'][3],correct_answer))
            #chr(j + ord('A')
            choices_buttons=[choices_A,choices_B,choices_C,choices_D]
            clock = pygame.time.Clock()
            timer_duration = 5000 
            elapsed_time = 0 
            font = pygame.font.Font(None, 36)
            while True:
                events = pygame.event.get()

                found_answer = False
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    for button in choices_buttons:
                        if event.button == 1:
                            found_answer = button.handle_event(event)
                              
                if found_answer:
                    self.user.correct_answer(1)
                    print(self.user.points)
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