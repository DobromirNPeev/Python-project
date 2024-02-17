from typing import override
from Button import Button
from TextBoxForFiles import TextBoxForFiles
from Constants import screen_height,screen_width,FIRST_ROUND_QUESTION_PATH
from AddQuestionMixin import AddQuestionMixin

class FirstRoundAddQuestion(AddQuestionMixin):

    def __init__(self):
        super().__init__(FIRST_ROUND_QUESTION_PATH)
        self._create_interface()

    @override
    def _create_interface(self):
        self.data={"question": "",
                   "choices": [],
                    "answer(s)": []}
        self.question_input=Button(screen_width//2-420,screen_height//2-250,200,50,"Question input:",lambda : None)
        self.type_question=TextBoxForFiles(screen_width//2-210,screen_height//2-240,200,50,"question",self.data)
        self.answers_input=Button(screen_width//2-420,screen_height//2-150,200,50,"Answers input:",lambda : None)
        self.type_answer_A=TextBoxForFiles(screen_width//2-210,screen_height//2-150,200,50,"choices",self.data)
        self.type_answer_B=TextBoxForFiles(screen_width//2-210,screen_height//2-90,200,50,"choices",self.data)
        self.type_answer_C=TextBoxForFiles(screen_width//2-210,screen_height//2-30,200,50,"choices",self.data)
        self.type_answer_D=TextBoxForFiles(screen_width//2-210,screen_height//2+30,200,50,"choices",self.data)
        self.correct_answer=Button(screen_width//2-420,screen_height//2+100,200,50,"Correct answer:",lambda : None)
        self.type_correct_answer=TextBoxForFiles(screen_width//2-210,screen_height//2+110,200,50,"answer(s)",self.data)
        self.done=Button(screen_width//2-100,screen_height//2+200,200,50,"Done",lambda : self._save_data())
        self.buttons=[self.question_input,self.type_question,self.answers_input, self.type_answer_A,self.type_answer_B,self.type_answer_C,self.type_answer_D,self.correct_answer,self.type_correct_answer,self.done]