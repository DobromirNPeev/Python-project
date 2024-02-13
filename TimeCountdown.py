import pygame
from Constants import screen_height,screen_width,WHITE

class TimeCountdown:
    def __init__(self,timer_duration,screen):
        self.clock = pygame.time.Clock()
        self.timer_duration = timer_duration 
        self.elapsed_time = 0 
        self.font = pygame.font.Font(None, 36)
        self.screen=screen
    
    def tick(self):
        dt = self.clock.tick(60)
        self.elapsed_time += dt
        remaining_time = max(self.timer_duration - self.elapsed_time, 0)
        self.remaining_seconds = remaining_time // 1000

    def draw_countdown(self):
        timer_text = self.font.render(f"Time remaining: {self.remaining_seconds} seconds", True, WHITE)
        timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height // 2+200))
        self.screen.blit(timer_text, timer_rect)

    def __bool__(self):
        return self.remaining_seconds>0

    def start_clock(self,background):
        while True:
            self.tick()
            if not self:
                break
            self.screen.blit(background, (0, 0))
            self.draw_countdown()
            pygame.display.flip()