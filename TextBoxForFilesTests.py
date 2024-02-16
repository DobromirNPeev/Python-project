import unittest
import pygame
from Constants import screen_height,screen_width,WHITE,BLACK
from TextBoxForFiles import TextBoxForFiles

class TextBoxForFilesTest(unittest.TestCase):

    def test_handle_event(self):
        pygame.init()
        self.data={"question": "",
                   "answer(s)": []}
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2-50,200,50,"question",self.data)
        click_on_text_box_event=pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        click_on_text_box_event.pos=self.type_question.rect.topleft
        original_active=self.type_question.active
        self.type_question.handle_event(click_on_text_box_event)
        self.assertEqual(not original_active,self.type_question.active)
        self.assertEqual(WHITE,self.type_question.color)
        click_on_text_box_event.pos=(0,5)
        self.type_question.handle_event(click_on_text_box_event)
        self.assertFalse(self.type_question.active)
        self.assertEqual(BLACK,self.type_question.color)
        text_box_event=pygame.event.Event(pygame.KEYDOWN)
        self.type_question.active=True
        text_box_event.key=pygame.K_RETURN
        self.type_question.text='something'
        self.type_question.handle_event(text_box_event)
        self.assertEqual(self.type_question.data[self.type_question.name],'something')
        self.assertEqual(self.type_question.text,'')
        self.type_question=TextBoxForFiles(screen_width//2,screen_height//2-50,200,50,"answer(s)",self.data)
        self.type_question.active = True
        self.list=['something']
        self.type_question.text='something'
        self.type_question.handle_event(text_box_event)
        self.assertEqual(self.type_question.data[self.type_question.name],self.list)
        self.assertEqual(self.type_question.text,'')
        text_box_event.key = pygame.K_BACKSPACE
        self.type_question.text='something'
        original_text=self.type_question.text
        self.type_question.handle_event(text_box_event)
        self.assertEqual(self.type_question.text,original_text[0:-1])
        text_box_event.unicode='G'
        text_box_event.key=None
        original_text=self.type_question.text
        self.type_question.handle_event(text_box_event)
        self.assertEqual(self.type_question.text,f"{original_text}G")

if __name__ == '__main__':
    unittest.main()