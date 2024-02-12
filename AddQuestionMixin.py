from LoadFiles import LoadFiles
from ScreenMixin import ScreenMixin

class AddQuestionMixin(ScreenMixin):

    def __init__(self,questions_path):
        super().__init__()
        self.loaded_data = LoadFiles.load_questions(questions_path)