from typing import override
from Button import Button
from TextBoxForFiles import TextBoxForFiles
from Constants import screen_height,screen_width,FIFTH_ROUND_QUESTION_PATH
from AddQuestionMixin import AddQuestionMixin

class FifthRoundAddQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__(FIFTH_ROUND_QUESTION_PATH)
        self._create_interface()

    @override
    def _create_interface(self):
        self.data={"question": "",
                   "answer(s)": []}
        self.question_input=Button(screen_width//2-420,screen_height//2-60,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2-210,screen_height//2-50,200,50,"question",self.data)
        self.correct_answer=Button(screen_width//2-420,screen_height//2+30,200,50,"Correct answer:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2-210,screen_height//2+40,200,50,"answer(s)",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self._save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answer,self.type_correct_answer,self.done]