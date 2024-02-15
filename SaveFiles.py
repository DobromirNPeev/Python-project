import json

class SaveFiles:

    @staticmethod
    def save_data(data,loaded_data,questions_path):
        from AddQuestionScreen import AddQuestionScreen
        for element in data.values():
            if not element:
                return AddQuestionScreen()    
        loaded_data.append(data)
        with open(questions_path, "w") as json_file:
            json.dump(loaded_data, json_file)
        return AddQuestionScreen()