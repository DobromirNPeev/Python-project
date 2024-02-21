from ThirdRound import ThirdRound
from Player import Player
from Button import Button
from TextBoxForQuestions import TextBoxForQuestions
import pygame
import unittest

class ThirdRoundTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.third_round = ThirdRound(Player())
        
    def test_create_interface(self):
        self.third_round.random_question = self.third_round._choose_random_question(self.third_round.loaded_data)
        self.third_round.correct_answers = self.third_round.random_question["answer(s)"]
        original_generated_questions = self.third_round.generated_questions
        self.third_round._create_interface()
        expected_attributes_for_singleplayer = {
                                                'objects':[self.third_round.question_text,self.third_round.skip_button,self.third_round.type_area],
                                                'found_answer' : None,
                                                'generated_questions':original_generated_questions+1
                                                }
        self.assertIsInstance(self.third_round.question_text,Button)
        self.assertIsInstance(self.third_round.type_area,TextBoxForQuestions) 
        self.assertIsInstance(self.third_round.skip_button,Button)
        instance_attributes = vars(self.third_round)
        for attr_name, expected_value in expected_attributes_for_singleplayer.items():
            self.assertTrue(attr_name in instance_attributes)
            self.assertEqual(instance_attributes[attr_name], expected_value)
        self.assertTrue(pygame.mixer.get_init(),True)
        self.assertIsInstance(self.third_round.sound,pygame.mixer.Sound)


if __name__=='__main__':
    unittest.main()
