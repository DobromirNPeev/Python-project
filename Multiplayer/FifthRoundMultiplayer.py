from typing import override
import pygame
from Button import Button
from textbox import TextBoxForQuestions
from Player import Player
from Constants import *
from MultiplayerRound import MultiplayerRound

class FifthRoundMultiplayer(MultiplayerRound):
    def __init__(self,player1,player2):
        from MainMenu import MainMenu
        super().__init__(FIFTH_ROUND_QUESTION_PATH,lambda : MainMenu(Player()),
                         POINTS_FOR_FIFTH_ROUND,
                         TIME_FOR_FIFTH_ROUND,
                         QUESTIONS_FOR_FIFTH_ROUND,
                         player1,player2)
    
    @override
    def _create_interface(self):
            self.player_turn=Button(screen_width//2 - 115,screen_height//2 + 225,250,50,f"{self.current_player.name}'s turn",lambda: None)
            self.question_text = Button(screen_width//2 - 230, screen_height//2 - 175,500,50,self.random_question['question'],lambda: None)
            self.type_area = TextBoxForQuestions(screen_width//2 - 115, screen_height//2 + 84,250,35,self._is_correct,self.random_question["answer(s)"])
            self.skip_button= Button(screen_width//2 - 65,screen_height//2 + 125,150,50,f"Skip",lambda: None)
            self.objects=[self.player_turn,self.question_text,self.skip_button,self.type_area]
            self.found_answer = None
            self.generated_questions+=1
