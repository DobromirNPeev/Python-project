import pygame
from tkinter import Tk, filedialog
import json
from pydub import AudioSegment

class OpenFiles:

    @staticmethod
    def open_image():
        root = Tk()
        root.withdraw()  # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        root.destroy()  # Destroy the Tkinter window after file selection
        if file_path:
            try:
                image = pygame.image.load(file_path)
                return image,file_path
            except pygame.error:
                print("Unable to load image:", file_path)
                return None
            
    @staticmethod
    def open_audio():
        root = Tk()
        root.withdraw()  # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
        root.destroy()  # Destroy the Tkinter window after file selection
        if file_path:
            try:
                audio = AudioSegment.from_file(file_path)
                return audio,file_path
            except pygame.error:
                print("Unable to load image:", file_path)
                return None