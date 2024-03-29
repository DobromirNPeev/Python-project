from Button import Button
from Constants import THIRD_ROUND_QUESTION_PATH,POINTS_FOR_THIRD_ROUND,TIME_FOR_THIRD_ROUND,QUESTIONS_FOR_THIRD_ROUND,AUDIO_PATH,screen_height,screen_width
from LoadFiles import LoadFiles
from Round import Round
from TextBoxForQuestions import TextBoxForQuestions
from FourthRound import FourthRound
import pygame


class ThirdRound(Round):

    def __init__(self,player):
        super().__init__(THIRD_ROUND_QUESTION_PATH,lambda : FourthRound(player),
                         POINTS_FOR_THIRD_ROUND,
                         TIME_FOR_THIRD_ROUND,
                         QUESTIONS_FOR_THIRD_ROUND,
                         player)
        self.loaded_data = LoadFiles.load_audio(self.loaded_data,AUDIO_PATH)

    def _create_interface(self):
        self.question_text = Button(screen_width // 2-222, screen_height // 2,500,50,f"{self.generated_questions+1}) {self.random_question['question']}",lambda: None)
        self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,self._is_correct,self.correct_answers)
        self.skip_button = Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
        self.objects = [self.question_text,self.skip_button,self.type_area]
        self.found_answer = None
        self.generated_questions+=1
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound((self.random_question['audio']-20).raw_data)
        self.sound.play()