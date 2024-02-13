from Button import Button
import pygame
from Constants import *
from LoadFiles import LoadFiles
from RoundBase import Round
from textbox import TextBoxForQuestions


class ThirdRound(Round):

    def __init__(self,player):
        from FourthRound import FourthRound
        super().__init__(THIRD_ROUND_QUESTION_PATH,lambda : FourthRound(player),
                         POINTS_FOR_THIRD_ROUND,
                         TIME_FOR_THIRD_ROUND,
                         QUESTIONS_FOR_THIRD_ROUND,
                         player)
        self.loaded_data=LoadFiles.load_audio(self.loaded_data,"D:/Python project/audio-files")

    def _create_interface(self):
        self.question_text = Button(screen_width // 2-222, screen_height // 2,500,50,self.random_question['question'],lambda: None)
        self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,self.correct_answers)
        self.skip_button= Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
        self.objects=[self.question_text,self.skip_button,self.type_area]
        self.found_answer = None
        self.generated_questions+=1
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound((self.random_question['audio']-20).raw_data)
        self.sound.play()