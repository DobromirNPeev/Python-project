from typing import override
from Button import Button
from TextBoxForFiles import TextBoxForFiles
from Constants import screen_height,screen_width,THIRD_ROUND_QUESTION_PATH,AUDIO_PATH
from AddQuestionMixin import AddQuestionMixin
from OpenFiles import OpenFiles
from FileCommands import FileCommands
import pygame

class ThirdRoundAddQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__(THIRD_ROUND_QUESTION_PATH)
        self._create_interface()

    @override
    def _create_interface(self):
        self.data={"file_path": "",
                   "question": '',
                    "answer(s)": []}
        self.open_audio_button=Button(screen_width//2-420,screen_height//2+10,200,50,"Open audio",lambda : self.open_audio())
        self.question_input=Button(screen_width//2-210,screen_height//2,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2+10,200,50,"question",self.data)
        self.correct_answer=Button(screen_width//2-210,screen_height//2+100,200,50,"Correct answers:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2,screen_height//2+110,200,50,"answer(s)",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self._save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answer,self.type_correct_answer,self.done,self.open_audio_button]
        self.audio= None

    def open_audio(self):
        if self.audio:
            self.sound.stop()
        self.audio,self.audio_path,self.original_path=OpenFiles.open_audio()
        self.data['file_path']=self.audio_path
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound((self.audio-30).raw_data)
        self.sound.play()

    @override
    def _save_data(self):
        if self.audio:
            self.sound.stop()
        next_screen = super()._save_data()
        FileCommands.move_file(self.original_path,AUDIO_PATH)
        return next_screen