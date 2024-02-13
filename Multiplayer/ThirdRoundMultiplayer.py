import pygame
from Button import Button
from textbox import TextBoxForQuestions
from LoadFiles import LoadFiles
from Constants import *
from MultiplayerRound import MultiplayerRound

class ThirdRoundMultiplayer(MultiplayerRound):

    def __init__(self,player1,player2):
        from FourthRoundMultiplayer import FourthRoundMultiplayer
        super().__init__(THIRD_ROUND_QUESTION_PATH,lambda : FourthRoundMultiplayer(player1,player2),
                         POINTS_FOR_THIRD_ROUND,
                         TIME_FOR_THIRD_ROUND,
                         QUESTIONS_FOR_THIRD_ROUND,
                         player1,player2)
        self.loaded_data=LoadFiles.load_audio(self.loaded_data,"D:/Python project/audio-files")

    def _create_interface(self):
        self.player_turn=Button(screen_width//2 - 115,screen_height//2 + 225,250,50,f"{self.current_player.name}'s turn",lambda: None)
        self.question_text = Button(screen_width//2 - 222, screen_height//2,500,50,self.random_question['question'],lambda: None)
        self.type_area = TextBoxForQuestions(screen_width//2 - 115, screen_height//2 + 84,250,35,self._is_correct,self.random_question["answer(s)"])
        self.skip_button= Button(screen_width//2-65,screen_height//2 + 125,150,50,f"Skip",lambda: None)
        self.objects=[self.player_turn,self.question_text,self.skip_button,self.type_area]
        self.found_answer = None
        audio=self.random_question['audio']
        self.generated_questions+=1
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound((audio-20).raw_data)
        self.sound.play()