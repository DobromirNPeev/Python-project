import pygame
from MainMenu import MainMenu
from User import User
from ScreenMixin import ScreenMixin

def main():
    pygame.init()
    WHITE = (255, 255, 255)

    user = User()

    running =True
    main_menu=MainMenu(user)

    pygame.init()

    current_screen=main_menu
    while True:
        events = pygame.event.get()

        # Handle events for the current screen
        for event in events: 
            for button in current_screen.buttons:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                next_screen=button.handle_event(event)
                if not pygame.get_init():
                    return
                if isinstance(next_screen,ScreenMixin):
                    break
            if isinstance(next_screen,ScreenMixin):
                    break
            
        # If a new screen is returned, switch to that screen
        if isinstance(next_screen,ScreenMixin):
            current_screen = next_screen

        # Draw buttons
        current_screen.render(current_screen.screen)
        if not pygame.get_init():
            return
        pygame.display.flip()
            # Pass events to buttons
        
if __name__== '__main__':
     main()
