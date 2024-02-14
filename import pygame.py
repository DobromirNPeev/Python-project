import pygame
from MainMenu import MainMenu
from Player import Player
from ScreenMixin import ScreenMixin

def main():
    pygame.init()

    user = Player()

    main_menu=MainMenu(user)

    pygame.init()

    current_screen=main_menu
    while True:
        events = pygame.event.get()
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
            
        if isinstance(next_screen,ScreenMixin):
            current_screen = next_screen

        current_screen.render(current_screen.screen)
        if not pygame.get_init():
            return
        pygame.display.flip()
        
if __name__== '__main__':
     main()
