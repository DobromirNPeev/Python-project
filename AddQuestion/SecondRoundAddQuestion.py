from typing import override
from Button import Button
from TextBox.TextBoxForFiles import TextBoxForFiles
from Constants import screen_height,screen_width,SECOND_ROUND_QUESTION_PATH
from AddQuestion.AddQuestionMixin import AddQuestionMixin
from FileManager.OpenFiles import OpenFiles

class SecondRoundAddQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__(SECOND_ROUND_QUESTION_PATH)
        self._create_interface()     
    
    @override
    def _create_interface(self):
        self.data={"question": "",
                   "file_path": '',
                    "answer(s)": []}
        self.open_image_button=Button(screen_width//2-420,screen_height//2+10,200,50,"Open image",lambda : self.open_image())
        self.question_input=Button(screen_width//2-210,screen_height//2,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2+10,200,50,"question",self.data)
        self.correct_answer=Button(screen_width//2-210,screen_height//2+100,200,50,"Correct answers:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2,screen_height//2+110,200,50,"answer(s)",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self._save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answer,self.type_correct_answer,self.done,self.open_image_button]
        self.image = None

    def open_image(self):
        self.image,self.image_path=OpenFiles.open_image()
        self.data['file_path']=self.image_path
    
    @override
    def render(self,screen):
        super().render(screen)
        if self.image:
            screen.blit(self.image,self.image.get_rect(center=(screen_width // 2, screen_height//2 - 150)))

    @override
    def _save_data(self):
        next_screen = super()._save_data()
        return next_screen