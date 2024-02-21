from Constants import screen_height,screen_width
from TextBoxForMultiplayer import TextBoxForMultiplayer
from Player import Player
import unittest
import pygame

class TextBoxForFilesTest(unittest.TestCase):

    def test_handle_event(self):
        pygame.init()
        self.text_box=TextBoxForMultiplayer(screen_width // 2-100, screen_height // 2-90,250,35,Player())
        text_box_event=pygame.event.Event(pygame.KEYDOWN)
        self.text_box.active=True
        text_box_event.key=pygame.K_RETURN
        self.text_box.text='something'
        self.text_box.handle_event(text_box_event)
        self.assertEqual(self.text_box.user.name,'something')
        

if __name__ == '__main__':
    unittest.main()