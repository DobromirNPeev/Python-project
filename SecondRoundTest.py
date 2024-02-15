import unittest
from Constants import SECOND_ROUND_QUESTION_PATH,POINTS_FOR_SECOND_ROUND,TIME_FOR_SECOND_ROUND,QUESTIONS_FOR_SECOND_ROUND,TERMINATED,VALID,SKIPPED,screen_height,screen_width
from SecondRound import SecondRound
from ThirdRound import ThirdRound
from Player import Player
from Button import Button
from TextBoxForQuestions import TextBoxForQuestions
import pygame

class SecondRoundTests(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.second_round=SecondRound(Player())
        
    def test_create_interface(self):
        self.second_round.random_question=self.second_round._choose_random_question(self.second_round.loaded_data)
        self.second_round.correct_answers = self.second_round.random_question["answer(s)"]
        original_generated_questions=self.second_round.generated_questions
        self.second_round._create_interface()
        expected_attributes_for_singleplayer = {
                                                'objects':[self.second_round.question_text,self.second_round.skip_button,self.second_round.type_area],
                                                'found_answer' : None,
                                                'generated_questions':original_generated_questions+1
                                                }
        self.assertIsInstance(self.second_round.question_text,Button)
        self.assertIsInstance(self.second_round.type_area,TextBoxForQuestions) 
        self.assertIsInstance(self.second_round.skip_button,Button)
        instance_attributes = vars(self.second_round)
        for attr_name, expected_value in expected_attributes_for_singleplayer.items():
            self.assertTrue(attr_name in instance_attributes)
            self.assertEqual(instance_attributes[attr_name], expected_value)

if __name__=='__main__':
    unittest.main()