import pygame
import pydub
import os
import json
from Constants import screen_height,screen_width

class LoadFiles:
    def __init__(self, questions_path):
        self.questions_path=questions_path

    def __load_multimedia_data(self,folder,file_type):
        for entry in self.loaded_data:
            question = entry['question']
            filename = entry['file_path']
            answers = entry['answers']

            path = os.path.join(folder, filename)
            if file_type == "images":
                element = pygame.image.load(path)
                self.image_data.append( {'question' : question, 'image': element, 'rect': element.get_rect(center=(screen_width // 2, screen_height // 2-150)), 'answers': answers})
            else:
                element = pydub.AudioSegment.from_file(path)
                self.audio_data.append( {'question' : question,'audio':element , 'answers': answers})
                

    def _load_questions(self):
        with open(self.questions_path, 'r') as file:
            self.loaded_data = json.load(file)

    def _load_images(self,image_folder):
        self._load_questions()
        self.image_data=[]
        self.__load_multimedia_data(image_folder,'images')

    def _load_audio(self,audio_folder):
        self._load_questions()
        self.audio_data = []
        self.__load_multimedia_data(audio_folder,'audio-files')