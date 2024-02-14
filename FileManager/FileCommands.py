import os

class FileCommands:
    @staticmethod
    def find_file_path(file_name):
        for root, dirs, files in os.walk('.'):
            if file_name in files:
                return os.path.join(root, file_name)
        return None
    
    @staticmethod
    def find_folder_path(folder_name):
        current_directory = os.getcwd()
        return os.path.join(current_directory, folder_name)