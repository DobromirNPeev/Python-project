from typing import override
import pygame
from Button import Button
from textbox import TextBoxForFiles
from tkinter import Tk, filedialog
import json
from pydub import AudioSegment
from ScreenMixin import ScreenMixin
from Constants import screen_height,screen_width
from AddQuestionMixin import AddQuestionMixin

WHITE = (255, 255, 255)

def open_image():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    root.destroy()  # Destroy the Tkinter window after file selection
    if file_path:
        try:
            image = pygame.image.load(file_path)
            return image,file_path
        except pygame.error:
            print("Unable to load image:", file_path)
            return None
            
def open_audio():
        root = Tk()
        root.withdraw()  # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
        root.destroy()  # Destroy the Tkinter window after file selection
        if file_path:
            try:
                audio = AudioSegment.from_file(file_path)
                return audio,file_path
            except pygame.error:
                print("Unable to load image:", file_path)
                return None

class AddQuestionScreen(AddQuestionMixin):
        
    def __init__(self):
        from MainMenu import MainMenu
        from User import User
        super().__init__()
        self.first_round_question_button = Button(screen_width//2-100,screen_height//2-250,200,50,"First Round Question",lambda : FirstRoundQuestion())
        self.second_round_question_button = Button(screen_width//2-100,screen_height//2-160,200,50,"Second Round Question",lambda : SecondRoundQuestion())
        self.third_round_question_button = Button(screen_width//2-100,screen_height//2-70,200,50,"Third Round Question",lambda : ThirdRoundQuestion())
        self.fourth_round_question_button = Button(screen_width//2-100,screen_height//2+20,200,50,"Fourth Round Question",lambda : FourthRoundQuestion())
        self.fifth_round_question_button = Button(screen_width//2-100,screen_height//2+110,200,50,"Fifth Round Question",lambda : FifthRoundQuestion())
        self.go_back_button = Button(screen_width//2-100,screen_height//2+210,200,50,"Go back",lambda : MainMenu(User()))
        self.buttons=[self.first_round_question_button,self.second_round_question_button,self.third_round_question_button,self.fourth_round_question_button,self.fifth_round_question_button,self.go_back_button]

class FirstRoundQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__("D:/Python project/firstround.json")
        self.data={"question": "",
                   "choices": [],
                    "correct_answer": []}
        self.question_input=Button(screen_width//2-210,screen_height//2-150,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2-140,200,50,"question",self.data)
        self.answers_input=Button(screen_width//2-100,screen_height//2-70,200,50,"Answers input:",lambda : None)
        self.type_answer_A=TextBoxForFiles(screen_width//2-420,screen_height//2+30,200,50,"choices",self.data)
        self.type_answer_B=TextBoxForFiles(screen_width//2-210,screen_height//2+30,200,50,"choices",self.data)
        self.type_answer_C=TextBoxForFiles(screen_width//2,screen_height//2+30,200,50,"choices",self.data)
        self.type_answer_D=TextBoxForFiles(screen_width//2+210,screen_height//2+30,200,50,"choices",self.data)
        self.correct_answer=Button(screen_width//2-210,screen_height//2+100,200,50,"Correct answer:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2,screen_height//2+110,200,50,"correct_answer",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self.save_data())
        self.buttons=[self.question_input,self.type_question,self.answers_input, self.type_answer_A,self.type_answer_B,self.type_answer_C,self.type_answer_D,self.correct_answer,self.type_correct_answer,self.done]
        with open("D:/Python project/firstround.json", 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)

    def save_data(self):
        for element in self.data.values():
            if not element:
                return AddQuestionScreen()
        self.loaded_data.append(self.data)
        with open("D:/Python project/firstround.json", "w") as json_file:
            json.dump(self.loaded_data, json_file)
        return AddQuestionScreen()

class SecondRoundQuestion(AddQuestionMixin):
    def __init__(self):
        super().__init__()
        self.data={"question": "",
                   "file_path": '',
                    "answers": []}
        self.open_image_button=Button(screen_width//2-420,screen_height//2+10,200,50,"Open image",lambda : self.draw_image())
        self.question_input=Button(screen_width//2-210,screen_height//2,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2+10,200,50,"question",self.data)
        self.correct_answer=Button(screen_width//2-210,screen_height//2+100,200,50,"Correct answers:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2,screen_height//2+110,200,50,"answers",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self.save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answer,self.type_correct_answer,self.done,self.open_image_button]
        self.image= None
        with open("D:/Python project/images/questionsforimages.json", 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)

    def draw_image(self):
        self.image,self.image_path=open_image()
        self.data['file_path']=self.image_path

    def save_data(self):
        for element in self.data.values():
            if not element:
                return AddQuestionScreen()
        self.loaded_data.append(self.data)
        with open("D:/Python project/images/questionsforimages.json", "w") as json_file:
            json.dump(self.loaded_data, json_file)
        return AddQuestionScreen()
    
    @override
    def render(self,screen):
        self.screen.fill(WHITE)
        screen.blit(self.background, (0, 0))
        if self.image:
            screen.blit(self.image,self.image.get_rect(center=(screen_width // 2, screen_height // 2-150)))
        for button in self.buttons:
            button.draw(screen)

class ThirdRoundQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__()
        self.data={"file_path": "",
                   "question": '',
                    "answers": []}
        self.open_audio_button=Button(screen_width//2-420,screen_height//2+10,200,50,"Open audio",lambda : self.get_audio())
        self.question_input=Button(screen_width//2-210,screen_height//2,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2+10,200,50,"question",self.data)
        self.correct_answer=Button(screen_width//2-210,screen_height//2+100,200,50,"Correct answers:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2,screen_height//2+110,200,50,"answers",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self.save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answer,self.type_correct_answer,self.done,self.open_audio_button]
        self.audio= None
        with open("D:/Python project/audio-files/audio-files.json", 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)

    def get_audio(self):
        self.audio,self.audio_path=open_audio()
        self.data['file_path']=self.audio_path

    def save_data(self):
        for element in self.data.values():
            if not element:
                return AddQuestionScreen()
        self.loaded_data.append(self.data)
        with open("D:/Python project/audio-files/audio-files.json", "w") as json_file:
            json.dump(self.loaded_data, json_file)
        return AddQuestionScreen()

class FourthRoundQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__()
        self.data={"question": "",
                   "answers": [],
                    "needed_answers": 0}
        self.question_input=Button(screen_width//2-210,screen_height//2-60,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2-50,200,50,"question",self.data)
        self.correct_answers=Button(screen_width//2-210,screen_height//2+30,200,50,"Correct answers:",lambda : None)
        self.type_correct_answers=TextBoxForFiles(screen_width//2,screen_height//2+40,200,50,"answers",self.data)
        self.type_needed_answers=TextBoxForFiles(screen_width//2,screen_height//2+120,200,50,"needed_answers",self.data)
        self.needed_answers=Button(screen_width//2-210,screen_height//2+110,200,50,"Needed answers:",lambda : None)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self.save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answers,self.type_correct_answers,self.type_needed_answers,self.needed_answers,self.done]
        with open("D:/Python project/openquestions.json", 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)

    def save_data(self):
        self.data["needed_answers"]=int(self.data["needed_answers"])
        for element in self.data.values():
            if not element:
                return AddQuestionScreen()
        self.loaded_data.append(self.data)
        with open("D:/Python project/openquestions.json", "w") as json_file:
            json.dump(self.loaded_data, json_file)
        return AddQuestionScreen()

class FifthRoundQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__()
        self.data={"question": "",
                   "answers": []}
        self.question_input=Button(screen_width//2-210,screen_height//2-60,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2-50,200,50,"question",self.data)
        self.correct_answer=Button(screen_width//2-210,screen_height//2+30,200,50,"Correct answer:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2,screen_height//2+40,200,50,"answer",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self.save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answer,self.type_correct_answer,self.done]
        with open("D:/Python project/hardquestions.json", 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)

    def save_data(self):
        for element in self.data.values():
            if not element:
                return AddQuestionScreen()
        self.loaded_data.append(self.data)
        with open("D:/Python project/hardquestions.json", "w") as json_file:
            json.dump(self.loaded_data, json_file)
        return AddQuestionScreen()