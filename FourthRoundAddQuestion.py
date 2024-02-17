from typing import override
from Button import Button
from TextBoxForFiles import TextBoxForFiles
from Constants import screen_height,screen_width,FOURTH_ROUND_QUESTION_PATH
from AddQuestionMixin import AddQuestionMixin

class FourthRoundAddQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__(FOURTH_ROUND_QUESTION_PATH)
        self._create_interface()

    @override
    def _create_interface(self):
        self.data={"question": "",
                   "answer(s)": [],
                    "needed_answers": 0}
        self.question_input=Button(screen_width//2-420,screen_height//2-110,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2-210,screen_height//2-100,200,50,"question",self.data)
        self.correct_answers=Button(screen_width//2-420,screen_height//2-30,200,50,"Correct answers:",lambda : None)
        self.type_correct_answers=TextBoxForFiles(screen_width//2-210,screen_height//2-20,200,50,"answer(s)",self.data)
        self.type_needed_answers=TextBoxForFiles(screen_width//2-210,screen_height//2+60,200,50,"needed_answers",self.data)
        self.needed_answers=Button(screen_width//2-420,screen_height//2+50,200,50,"Needed answers:",lambda : None)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self._save_data())
        self.buttons=[self.question_input,self.type_question,self.correct_answers,self.type_correct_answers,self.type_needed_answers,self.needed_answers,self.done]

    @override
    def _save_data(self):
        self.data["needed_answers"]=int(self.data["needed_answers"])
        return super()._save_data()