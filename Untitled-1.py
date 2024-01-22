class Round:
    def __init__(self, questions=""):
        self.questions_and_answers = {}
        with open(questions) as file_questions:
            for line in file_questions:
                question,answer = line.split('?')
                self.questions_and_answers[question]=answer
    
    def __repr__(self):
        for question,answer in self.questions_and_answers.items():
            print(question)
            print(answer)

round = Round("D:/Python project/firstround.txt")
print(round)