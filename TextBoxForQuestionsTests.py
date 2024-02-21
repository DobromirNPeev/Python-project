from Constants import screen_height,screen_width
from TextBoxForQuestions import TextBoxForQuestions
from InvalidArgumentException import InvalidArgumentException
import unittest
import pygame


class TextBoxForFilesTest(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(InvalidArgumentException):
            type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,lambda x: x+1,'random')
        with self.assertRaises(InvalidArgumentException):
            type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,lambda x,y,z: x+y+z,'random')
        self.assertIsInstance(TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,lambda x,y: x+y,'random'),TextBoxForQuestions)

    def test_handle_event(self):
        pygame.init()
        self.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,lambda x,y: x==y,'random')
        text_box_event = pygame.event.Event(pygame.KEYDOWN)
        self.type_area.active = True
        text_box_event.key = pygame.K_RETURN
        self.type_area.text = 'something'
        result = self.type_area.handle_event(text_box_event)
        self.assertFalse(result)
        self.type_area.text='random'
        result = self.type_area.handle_event(text_box_event)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()