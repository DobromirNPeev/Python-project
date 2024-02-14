import pygame
from tkinter import Tk, filedialog
from pydub import AudioSegment
import os

class OpenFiles:

    @staticmethod
    def open_image():
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        root.destroy() 
        if file_path:
            try:
                image = pygame.image.load(file_path)
                return image,os.path.basename(file_path),file_path
            except pygame.error:
                print("Unable to load image:", file_path)
                return None
            
    @staticmethod
    def open_audio():
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
        root.destroy()
        if file_path:
            try:
                audio = AudioSegment.from_file(file_path)
                return audio,os.path.basename(file_path),file_path
            except BaseException:
                print("Unable to load image:", file_path)
                return None