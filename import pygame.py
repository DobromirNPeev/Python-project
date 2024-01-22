import pygame
from MainMenu import MainMenu, PreGameScreen
from Round import FirstRound,ImageRound
from User import User

WHITE = (255, 255, 255)

user = User()

main_menu=MainMenu(user)

pygame.init()
font = pygame.font.Font(None, 36)

current_screen=main_menu
screen_width, screen_height = 1000, 600
while True:
    events = pygame.event.get()

    # Handle events for the current screen
    for event in events: 
        for button in current_screen.buttons:
            if event.type == pygame.QUIT:
                pygame.quit()
            next_screen=button.handle_event(event)
            if isinstance(next_screen,PreGameScreen) or isinstance(next_screen,MainMenu) or isinstance(next_screen,FirstRound) or isinstance(next_screen,ImageRound):
                break
        if isinstance(next_screen,PreGameScreen) or isinstance(next_screen,MainMenu) or isinstance(next_screen,FirstRound) or isinstance(next_screen,ImageRound):
                break
        
    # If a new screen is returned, switch to that screen
    if isinstance(next_screen,PreGameScreen) or isinstance(next_screen,MainMenu) or isinstance(next_screen,FirstRound) or isinstance(next_screen,ImageRound):
        current_screen = next_screen

    # Draw buttons
    current_screen.render(current_screen.screen)
    pygame.display.flip()
        # Pass events to buttons