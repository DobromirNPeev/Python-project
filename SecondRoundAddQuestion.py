from typing import override
from Button import Button
from TextBoxForFiles import TextBoxForFiles
from Constants import screen_height,screen_width,SECOND_ROUND_QUESTION_PATH,IMAGES_PATH
from AddQuestionMixin import AddQuestionMixin
from OpenFiles import OpenFiles
from FileCommands import FileCommands
from SaveFiles import SaveFiles

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
        self.constraints=Button(screen_width//2-420,screen_height//2+70,200,50,f"Should have width less than {screen_width} and height less than {screen_height//2}",lambda : None)
        self.buttons=[self.question_input,self.type_question,self.correct_answer,self.type_correct_answer,self.done,self.open_image_button,self.constraints]
        self.image = None

    def open_image(self):
        self.image,self.image_path,self.original_path=OpenFiles.open_image()
        if self.image.get_width() > screen_width or self.image.get_height() > screen_height // 2:
            self.image = None
            self.image_path = None
            self.original_path = None
            return
        self.data['file_path']=self.image_path
    
    @override
    def render(self,screen):
        super().render(screen)
        if self.image:
            screen.blit(self.image,self.image.get_rect(center=(screen_width // 2, screen_height//2 - 150)))

    @override
    def _save_data(self):
        next_screen,successful = SaveFiles.save_data(self.data,self.loaded_data,self.question_path)
        if successful:
            FileCommands.move_file(self.original_path,IMAGES_PATH)
        return next_screen