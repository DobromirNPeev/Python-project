import json
import random

#"D:/Python project/firstround.json"
class Round:
    def __init__(self, questions):
        with open(questions, 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)
            
    @staticmethod
    def choose_random_question(questions):
        return random.choice(questions)

round=Round("D:/Python project/firstround.json")

random_question = round.choose_random_question(round.loaded_data)

print(f"\nRandom Question: {random_question['question']}")
for i, choice in enumerate(random_question['choices'], start=1):
    print(f"{i}. {choice}")

user_answer = input("Your answer: ")
correct_answer = random_question['correct_answer']

if user_answer.lower() == correct_answer.lower():
    print("Correct!")
else:
    print(f"Wrong! The correct answer is {correct_answer}.")
