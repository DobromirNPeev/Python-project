import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Typing Window with Pygame')

# Set up fonts
font = pygame.font.Font(None, 36)

# Initialize variables
text = ""
text_color = (0, 0, 0)
input_active = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Handle Enter key (you can add more logic here)
                print("Typed:", text)
                text = ""
            elif event.key == pygame.K_BACKSPACE:
                # Handle Backspace key
                text = text[:-1]
            elif event.key == pygame.K_ESCAPE:
                # Handle Escape key to toggle input focus
                input_active = not input_active
            else:
                # Handle other key presses
                text += event.unicode

    # Clear the screen
    screen.fill((255, 255, 255))

    # Display the text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)

    # Draw a cursor if input is active
    if input_active and pygame.time.get_ticks() % 1000 < 500:
        cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
        pygame.draw.rect(screen, text_color, cursor_rect)

    # Update the display
    pygame.display.flip()
