from Round import Round,getMidPoint,Button,WHITE
import pygame

class OpenQuestions(Round):
    def __init__(self,user):
        super().__init__("D:/Python project/firstround.json")
        self.font = pygame.font.Font(None, 36)
        self.screen_width, self.screen_height = 1000, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("D:/Python project/logo_www-k9vmwvd2.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame Screen Example")
        self.screen=pygame.display.set_mode((self.screen_width, self.screen_height))
        self.midPoint=getMidPoint(0,0,800,600)
        self.copy_questions=copy.deepcopy(self.loaded_data)
        self.user = user
        midPoint=getMidPoint(0,0,800,600)
        self.continue_button = Button(midPoint[0],midPoint[1]-50,200,50,"Continue",lambda : self.generate_second_round())
        self.buttons=[self.continue_button]
        self.generated_questions=0
    
    def 
    def render(self,screen):
        screen.fill(WHITE)
        if self.generated_questions<9:
            for self.generated_questions in range(0,10):
                random_question=Round.choose_random_question(self.image_data)
                correct_answers = random_question["correct_answer"]
                question_text = Button(self.screen_width // 2-222, self.screen_height // 2,500,50,random_question['question'],lambda: None)
                type_area = Button(self.screen_width // 2-115, self.screen_height // 2+84,250,35,"",lambda: None)
                clock = pygame.time.Clock()
                timer_duration = 1000 
                elapsed_time = 0 
                font = pygame.font.Font(None, 36)
                found_answer = None
                text=''
                print(self.generated_questions)
                while True:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                found_answer=self.is_correct(text,correct_answers)
                                text = ""
                            elif event.key == pygame.K_BACKSPACE:
                                # Handle Backspace key
                                text = text[:-1]
                            else:
                                # Handle other key presses
                                text += event.unicode
                        
                    dt = clock.tick(60)  # Adjust the argument based on your desired frame rate
                    elapsed_time += dt

                    # Calculate remaining time
                    remaining_time = max(timer_duration - elapsed_time, 0)

                    # Convert remaining time to seconds
                    remaining_seconds = remaining_time // 1000
                    if remaining_seconds<=0:
                        break
                    self.screen.blit(self.background, (0, 0))
                    question_text.draw(self.screen)
                    type_area.draw(self.screen)
                    timer_text = font.render(f"Time remaining: {remaining_seconds} seconds", True, WHITE)
                    timer_rect = timer_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2+200))
                    self.screen.blit(timer_text, timer_rect)
                    text_surface = font.render(text, True, (0,0,0))
                    text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2+100))
                    screen.blit(text_surface, text_rect)
                    cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
                    pygame.draw.rect(screen, (0,0,0), cursor_rect)
                    screen.blit(random_question['image'],random_question['rect'])
                    pygame.display.flip()

                    if found_answer is True:
                        self.user.correct_answer(2)
                        print(self.user.points)
                        break
        else:
            self.screen.blit(self.background, (0, 0))
            self.continue_button.draw(self.screen)