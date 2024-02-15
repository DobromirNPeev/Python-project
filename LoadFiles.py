import pygame
import pydub
import os
import json
from Constants import screen_height,screen_width

class LoadFiles:

    @staticmethod
    def __load_multimedia_data(loaded_data,folder,file_type):
        multimedia_data = []
        for entry in loaded_data:
            question = entry['question']
            filename = entry['file_path']
            answers = entry['answer(s)']

            path = os.path.join(folder, filename)
            if file_type == "images":
                element = pygame.image.load(path)
                multimedia_data.append( {'question' : question, 'image': element, 'rect': element.get_rect(center=(screen_width // 2, screen_height // 2-150)), 'answer(s)': answers})
            else:
                element = pydub.AudioSegment.from_file(path)
                multimedia_data.append( {'question' : question,'audio':element , 'answer(s)': answers})
        return multimedia_data
                
    @staticmethod
    def load_questions(questions_path):
        with open(questions_path, 'r') as file:
            loaded_data = json.load(file)
        return loaded_data

    @staticmethod
    def load_images(loaded_data,image_folder):
        return LoadFiles.__load_multimedia_data(loaded_data,image_folder,'images')

    @staticmethod
    def load_audio(loaded_data,audio_folder):
        return LoadFiles.__load_multimedia_data(loaded_data,audio_folder,'audio-files')