import pygame
import os
from tkinter import Tk, filedialog

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Image Viewer")

# Colors
WHITE = (255, 255, 255)

def open_image():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    root.destroy()  # Destroy the Tkinter window after file selection
    if file_path:
        try:
            image = pygame.image.load(file_path)
            return image
        except pygame.error:
            print("Unable to load image:", file_path)
            return None

def main():
    image = open_image()
    if not image:
        return
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear the screen
        window.fill(WHITE)
        
        # Draw the image
        window.blit(image, (0, 0))

        # Update the display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
