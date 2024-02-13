from typing import override
from Button import Button
import pygame
from Player import Player
from Constants import *
from LoadFiles import LoadFiles
from RoundBase import Round
from textbox import TextBoxForQuestions

class SecondRound(Round):
    
    def __init__(self,player):
        from ThirdRound import ThirdRound
        super().__init__(SECOND_ROUND_QUESTION_PATH,lambda: ThirdRound(player),
                         POINTS_FOR_SECOND_ROUND,
                         TIME_FOR_SECOND_ROUND,
                         QUESTIONS_FOR_SECOND_ROUND,
                         player)
        self.loaded_data=LoadFiles.load_images(self.loaded_data,"D:/Python project/images")

    @override
    def _create_interface(self):
        self.question_text = Button(screen_width // 2-222,screen_height // 2,500,50,self.random_question['question'],lambda: None)
        self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,self.correct_answers)
        self.skip_button= Button(screen_width//2-65,screen_height // 2+125,150,50,f"Skip",lambda: None)
        self.objects=[self.question_text,self.skip_button,self.type_area]
        self.found_answer = None
        self.generated_questions+=1

    @override
    def _render_interface(self,screen):
        Round._render_interface(self,screen)
        screen.blit(self.random_question['image'],self.random_question['rect'])