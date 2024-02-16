import os
import shutil

class FileCommands:

    @staticmethod
    def find_file_path_in_current_directory(file_name):
        for root, _, files in os.walk('/'):
            if file_name in files:
                return os.path.join(root, file_name)
    
    @staticmethod
    def find_folder_path(folder_name):
        current_directory = os.getcwd()
        return os.path.join(current_directory, folder_name)
    
        
    @staticmethod
    def move_file(questions_path,folder_name):
        shutil.move(questions_path,FileCommands.find_folder_path(folder_name))