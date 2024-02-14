from FileManager.LoadFiles import LoadFiles
from ScreenMixin import ScreenMixin
from FileManager.SaveFiles import SaveFiles

class AddQuestionMixin(ScreenMixin):

    def __init__(self,questions_path):
        super().__init__() 
        self.loaded_data = LoadFiles.load_questions(questions_path)
        self.question_path=questions_path

    def _save_data(self):
        return SaveFiles.save_data(self.data,self.loaded_data,self.question_path)

    def _create_interface(self):
        pass
    
    