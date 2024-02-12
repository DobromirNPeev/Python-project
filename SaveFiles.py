import json
from LoadFiles import LoadFiles

class SaveFiles:
    def __init__(self,source):
        with open(source, 'r') as file:
            self.loaded_data = json.load(file)
            print(self.loaded_data)

    @staticmethod
    def save_data(data,loaded_data):
        from AddQuestions import AddQuestionScreen
        for element in data.values():
            if not element:
                return AddQuestionScreen()
        loaded_data.append(data)
        with open("D:/Python project/firstround.json", "w") as json_file:
            json.dump(loaded_data, json_file)
        return AddQuestionScreen()