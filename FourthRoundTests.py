import unittest
from Constants import FOURTH_ROUND_QUESTION_PATH,POINTS_FOR_FOURTH_ROUND,TIME_FOR_FOURTH_ROUND,QUESTIONS_FOR_FOURTH_ROUND,TERMINATED,VALID,SKIPPED,screen_height,screen_width
from FourthRound import FourthRound
from FifthRound import FifthRound
from Player import Player
from Button import Button
from TextBoxForQuestions import TextBoxForQuestions
import pygame

class FourthRoundTests(unittest.TestCase):

        def setUp(self):
            pygame.init()
            self.fourth_round=FourthRound(Player())
            self.fourth_round.random_question=self.fourth_round._choose_random_question(self.fourth_round.loaded_data)
            self.fourth_round.correct_answers = self.fourth_round.random_question["answer(s)"]
    
        def test_create_interface(self):
            original_generated_questions=self.fourth_round.generated_questions
            self.fourth_round._create_interface()
            expected_attributes_for_singleplayer = {'needed_answers':self.fourth_round.random_question['needed_answers'],
                                                    'correct_answered':0,
                                                    'objects':[self.fourth_round.question_text,self.fourth_round.skip_button,self.fourth_round.type_area],
                                                    'found_answer' : None,
                                                    'generated_questions':original_generated_questions+1
                                                    }
            self.assertIsInstance(self.fourth_round.question_text,Button)
            self.assertIsInstance(self.fourth_round.type_area,TextBoxForQuestions) 
            self.assertIsInstance(self.fourth_round.skip_button,Button)
            instance_attributes = vars(self.fourth_round)
            for attr_name, expected_value in expected_attributes_for_singleplayer.items():
                self.assertTrue(attr_name in instance_attributes)
                self.assertEqual(instance_attributes[attr_name], expected_value)
        
        def test_check_for_correct_answers(self):
             self.fourth_round.found_answer=False
             self.fourth_round._create_interface()
             self.assertFalse(self.fourth_round._check_for_correct_answer())
             self.fourth_round.found_answer=True
             self.original_correct_answered= self.fourth_round.correct_answered
             self.fourth_round._check_for_correct_answer()
             self.assertEqual(self.original_correct_answered+1,self.fourth_round.correct_answered)
             self.fourth_round.found_answer=True
             self.fourth_round.correct_answered=0
             self.fourth_round.needed_answers=1
             self.original_points = self.fourth_round.current_player.points
             self.assertTrue(self.fourth_round._check_for_correct_answer())
             self.assertEqual(self.fourth_round.current_player.points,self.original_points+self.fourth_round.points_for_round)


                
if __name__=='__main__':
     unittest.main()