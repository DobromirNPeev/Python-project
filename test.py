import os
import json
from pydub import AudioSegment

class YourClass:
    def __init__(self):
        self.audio_data = []

    def load_audio_from_folder(self, audio_folder, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

        self.audio_data = []
        for entry in data['audio_files']:
            question = entry['question']
            audio_filename = entry['file_path']
            answer = entry['answer']

            audio_path = os.path.join(audio_folder, audio_filename)
            audio = AudioSegment.from_file(audio_path,format='mp3')

            self.audio_data.append({'question': question,  'correct_answer': answer})

# Example usage
your_instance = YourClass()
your_instance.load_audio_from_folder("D:/Python project/audio-files","D:/Python project/audio-files/audio-files.json")

# Accessing the loaded audio dat