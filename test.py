import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Checkbox")

# Define constants
CHECKBOX_SIZE = 20
PADDING = 10

# Define checkbox class
class Checkbox:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.checked = False

    def draw(self):
        checkbox_rect = pygame.Rect(self.x, self.y, CHECKBOX_SIZE, CHECKBOX_SIZE)
        pygame.draw.rect(screen, BLACK, checkbox_rect, 2)

        if self.checked:
            pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x + CHECKBOX_SIZE, self.y + CHECKBOX_SIZE), 2)
            pygame.draw.line(screen, BLACK, (self.x, self.y + CHECKBOX_SIZE), (self.x + CHECKBOX_SIZE, self.y), 2)

        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.x + CHECKBOX_SIZE + PADDING, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            checkbox_rect = pygame.Rect(self.x, self.y, CHECKBOX_SIZE, CHECKBOX_SIZE)
            if checkbox_rect.collidepoint(mouse_pos):
                self.checked = not self.checked

# Create checkbox instance
checkbox = Checkbox(50, 50, "Checkbox")

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        checkbox.handle_event(event)

    checkbox.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
