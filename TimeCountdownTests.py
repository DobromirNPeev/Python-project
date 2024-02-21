import unittest
import pygame
from Constants import screen_height,screen_width,BACKGROUND_PATH
from TimeCountdown import TimeCountdown
import time

class TimeCountdownTests(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.background = pygame.image.load(BACKGROUND_PATH)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.timer = TimeCountdown(2000,self.screen)
    
    def test_tick(self):
        original_elapsed_time = self.timer.elapsed_time
        self.timer.tick()
        self.assertNotEqual(original_elapsed_time,self.timer.elapsed_time+1)
        self.assertIn('remaining_seconds',vars(self.timer))

    def test_bool(self):
        self.assertFalse(self.timer)
        self.timer.remaining_seconds=-5
        self.assertFalse(self.timer)
        self.timer.remaining_seconds=9
        self.assertTrue(self.timer)

    def test_start_clock(self):
        start_time = time.time()
        self.timer.start_clock(self.background)
        current_time = time.time()
        elapsed_seconds = current_time - start_time
        self.assertEqual((2000-1000)//1000,int(elapsed_seconds))
        

if __name__=='__main__':
    unittest.main()