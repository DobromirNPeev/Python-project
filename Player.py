from InvalidArgumentException import InvalidArgumentException

class Player:
    def __init__(self,name=""):
        self.points = 0
        self.name = name

    def correct_answer(self,num):
        if num < 0:
            raise InvalidArgumentException
        self.points += num