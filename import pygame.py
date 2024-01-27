import pygame
from MainMenu import MainMenu, PreGameScreen
from Round import FirstRound,ImageRound,AudioRound,OpenQuestions,HardQuestions
from User import User
from AddQuestions import AddQuestionScreen,FirstRoundQuestion,SecondRoundQuestion,ThirdRoundQuestion,FourthRoundQuestion,FifthRoundQuestion
from Multiplayer import PreScreenMutliplayer,FirstRoundMultiplayer,ImageRoundMultiplayer,AudioRoundMultiplayer,OpenQuestionsMultiplayer,HardQuestionsMultiplayer

def main():
    pygame.init()
    WHITE = (255, 255, 255)

    user = User()

    running =True
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
                    return
                next_screen=button.handle_event(event)
                if isinstance(next_screen,PreGameScreen) or isinstance(next_screen,MainMenu) or isinstance(next_screen,FirstRound) or isinstance(next_screen,ImageRound) or isinstance(next_screen,AudioRound) or isinstance(next_screen,OpenQuestions) or isinstance(next_screen,ImageRound) or isinstance(next_screen,AudioRound) or isinstance(next_screen,HardQuestions) or isinstance(next_screen,AddQuestionScreen) or isinstance(next_screen,FirstRoundQuestion) or isinstance(next_screen,SecondRoundQuestion) or isinstance(next_screen,ThirdRoundQuestion) or isinstance(next_screen,FourthRoundQuestion) or isinstance(next_screen,FifthRoundQuestion) or isinstance(next_screen,PreScreenMutliplayer) or isinstance(next_screen,FirstRoundMultiplayer) or isinstance(next_screen,ImageRoundMultiplayer) or isinstance(next_screen,AudioRoundMultiplayer) or isinstance(next_screen,OpenQuestionsMultiplayer) or isinstance(next_screen,HardQuestionsMultiplayer):
                    break
            if isinstance(next_screen,PreGameScreen) or isinstance(next_screen,MainMenu) or isinstance(next_screen,FirstRound) or isinstance(next_screen,ImageRound) or isinstance(next_screen,AudioRound) or isinstance(next_screen,OpenQuestions) or isinstance(next_screen,ImageRound) or isinstance(next_screen,AudioRound) or isinstance(next_screen,HardQuestions) or isinstance(next_screen,AddQuestionScreen) or isinstance(next_screen,FirstRoundQuestion) or isinstance(next_screen,SecondRoundQuestion) or isinstance(next_screen,ThirdRoundQuestion) or isinstance(next_screen,FourthRoundQuestion) or isinstance(next_screen,FifthRoundQuestion) or isinstance(next_screen,PreScreenMutliplayer) or isinstance(next_screen,FirstRoundMultiplayer) or isinstance(next_screen,ImageRoundMultiplayer) or isinstance(next_screen,AudioRoundMultiplayer) or isinstance(next_screen,OpenQuestionsMultiplayer) or isinstance(next_screen,HardQuestionsMultiplayer):
                    break
            
        if not pygame.get_init():
            return
        # If a new screen is returned, switch to that screen
        if isinstance(next_screen,PreGameScreen) or isinstance(next_screen,MainMenu) or isinstance(next_screen,FirstRound) or isinstance(next_screen,ImageRound) or isinstance(next_screen,AudioRound) or isinstance(next_screen,OpenQuestions) or isinstance(next_screen,AudioRound) or isinstance(next_screen,HardQuestions) or isinstance(next_screen,AddQuestionScreen) or isinstance(next_screen,FirstRoundQuestion) or isinstance(next_screen,SecondRoundQuestion) or isinstance(next_screen,ThirdRoundQuestion) or isinstance(next_screen,FourthRoundQuestion) or isinstance(next_screen,FifthRoundQuestion) or isinstance(next_screen,PreScreenMutliplayer) or isinstance(next_screen,FirstRoundMultiplayer) or isinstance(next_screen,ImageRoundMultiplayer) or isinstance(next_screen,AudioRoundMultiplayer) or isinstance(next_screen,OpenQuestionsMultiplayer) or isinstance(next_screen,HardQuestionsMultiplayer):
            current_screen = next_screen

        # Draw buttons
        current_screen.render(current_screen.screen)
        if not pygame.get_init():
            return
        pygame.display.flip()
            # Pass events to buttons
        
if __name__== '__main__':
     main()
