
class Player:
    def __init__(self,name=""):
        self.points=0
        self.name=name

    def correct_answer(self,num):
        self.points+=num