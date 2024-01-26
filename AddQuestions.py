import pygame
from Button import Button
from textbox import TextBox
from tkinter import Tk, filedialog
import json

WHITE = (255, 255, 255)

def open_image():
        root = Tk()
        root.withdraw()  # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        root.destroy()  # Destroy the Tkinter window after file selection
        if file_path:
            try:
                image = pygame.image.load(file_path)
                return image
            except pygame.error:
                print("Unable to load image:", file_path)
                return None

class AddQuestionScreen:

        
    def __init__(self):
        self.screen_width, self.screen_height = 1000, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.first_round_question_button = Button(self.screen_width//2-100,self.screen_height//2-200,200,50,"First Round Question",lambda : self.generate_first_round_question_input())
        self.first_round_question_button = Button(self.screen_width//2-100,self.screen_height//2-200,200,50,"Second Round Question",lambda : self.generate_second_round_question_input())

       # multiplayer = Button(midPoint[0],midPoint[1]+25,200,50,"Multiplayer",lambda : print("OK1"))
       # add_quesiton = Button(midPoint[0],midPoint[1]+100,200,50,"Add question",lambda : print("OK2"))
       # exit = Button(midPoint[0],midPoint[1]+175,200,50,"Exit",lambda: pygame.quit())
        self.buttons=[self.first_round_question_button]

    def generate_second_round_question_input():
        return

    def generate_first_round_question_input(self):
        return FirstRoundQuestion()

    def render(self,screen):
        self.screen.fill((255,255,255))
        screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(screen)

class FirstRoundQuestion:

    def __init__(self):
        self.screen_width, self.screen_height = 1000, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.data={"question": "",
                   "choices": [],
                    "correct_answer": ""}
        self.question_input=Button(self.screen_width//2-100,self.screen_height//2-250,200,50,"Question input:",lambda : None)
        self.type_question=TextBox(self.screen_width//2-100,self.screen_height//2-150,200,50,"question",self.data)
        self.answers_input=Button(self.screen_width//2-100,self.screen_height//2-70,200,50,"Answers input:",lambda : None)
        self.type_answer_A=TextBox(self.screen_width//2-420,self.screen_height//2+30,200,50,"choices",self.data)
        self.type_answer_B=TextBox(self.screen_width//2-210,self.screen_height//2+30,200,50,"choices",self.data)
        self.type_answer_C=TextBox(self.screen_width//2,self.screen_height//2+30,200,50,"choices",self.data)
        self.type_answer_D=TextBox(self.screen_width//2+210,self.screen_height//2+30,200,50,"choices",self.data)
        self.correct_answer=Button(self.screen_width//2-210,self.screen_height//2+100,200,50,"Correct answer:",lambda : None)
        self.type_correct_answer=TextBox(self.screen_width//2,self.screen_height//2+110,200,50,"correct_answer",self.data)
        self.done=Button(self.screen_width//2-100,self.screen_height//2+200,200,50,"Done",lambda : self.save_data())
        self.buttons=[self.question_input,self.type_question,self.answers_input, self.type_answer_A,self.type_answer_B,self.type_answer_C,self.type_answer_D,self.correct_answer,self.type_correct_answer,self.done]
        with open("D:/Python project/firstround.json", 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)
        pygame.display.set_caption("Pygame Screen Example")

    def save_data(self):
        self.loaded_data.append(self.data)
        with open("D:/Python project/firstround.json", "w") as json_file:
            json.dump(self.loaded_data, json_file)
        return AddQuestionScreen()

    def render(self,screen):
        self.screen.fill(WHITE)
        screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.draw(screen)

class SecondRoundQuestion:
    pass