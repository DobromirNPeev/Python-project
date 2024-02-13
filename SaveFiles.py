import json
import os
import shutil

class SaveFiles:

    @staticmethod
    def save_data(data,loaded_data,questions_path):
        from AddQuestions import AddQuestionScreen
        for element in data.values():
            if not element:
                return AddQuestionScreen()
        
        loaded_data.append(data)
        with open(questions_path, "w") as json_file:
            json.dump(loaded_data, json_file)
        return AddQuestionScreen()
    
    @staticmethod
    def _move_file(questions_path):
        script_directory = os.path.dirname(__file__)
        destination_folder = os.path.join(script_directory, "images")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.move(questions_path, destination_folder)