import unittest
from Constants import TERMINATED,VALID,SKIPPED
from FirstRound import FirstRound
from Player import Player
from Button import Button
import pygame

pygame.init()

class TestFirstRound(unittest.TestCase):
    
    def setUp(self):
        self.first_round=FirstRound(Player())
        
    def test_create_interface(self):
        self.first_round.random_question=self.first_round._choose_random_question(self.first_round.loaded_data)
        self.first_round.correct_answers = self.first_round.random_question["answer(s)"]
        original_generated_questions=self.first_round.generated_questions
        self.first_round._create_interface()
        expected_attributes_for_singleplayer = {
                                                'objects' : [self.first_round.choices_A,self.first_round.choices_B,self.first_round.choices_C,self.first_round.choices_D,self.first_round.skip_button,self.first_round.question_text],
                                                'found_answer' : None,
                                                'generated_questions':original_generated_questions+1
                                                }
        for object in self.first_round.objects:
            self.assertIsInstance(object,Button) 
        instance_attributes = vars(self.first_round)
        for attr_name, expected_value in expected_attributes_for_singleplayer.items():
            self.assertTrue(attr_name in instance_attributes)
            self.assertEqual(instance_attributes[attr_name], expected_value)

    def test_check_for_correct_answer(self):
        self.first_round.found_answer=None
        self.assertFalse(self.first_round._check_for_correct_answer())
        self.first_round.found_answer=False
        self.assertTrue(self.first_round._check_for_correct_answer())
    
    def test_handle_events(self):
        self.first_round.random_question=self.first_round._choose_random_question(self.first_round.loaded_data)
        quit_event = pygame.event.Event(pygame.QUIT)
        self.assertEqual(TERMINATED,self.first_round._handle_events([quit_event]))
        pygame.init()
        skip_event=pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        skip_event.button=1
        self.first_round._create_interface()
        skip_event.pos = self.first_round.skip_button.rect.topleft
        self.assertEqual(SKIPPED,self.first_round._handle_events([skip_event]))
        choice_event=pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        choice_event.button=1
        choice_event.pos = self.first_round.choices_A.rect.topleft
        self.assertEqual(VALID,self.first_round._handle_events([choice_event]))
        random_event_1 = pygame.event.Event(pygame.APP_DIDENTERFOREGROUND)
        random_event_2 = pygame.event.Event(pygame.CONTROLLER_AXIS_LEFTY)
        self.assertEqual(VALID,self.first_round._handle_events([random_event_1,random_event_2]))
        self.assertEqual(VALID,self.first_round._handle_events([]))

        

if __name__ == '__main__':
    unittest.main()