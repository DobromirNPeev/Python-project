from Round import Round
from Constants import FIRST_ROUND_QUESTION_PATH,POINTS_FOR_FIRST_ROUND,TIME_FOR_FIRST_ROUND,QUESTIONS_FOR_FIRST_ROUND,TERMINATED,VALID,SKIPPED,screen_height,screen_width
from SecondRound import SecondRound
from Player import Player
from LoadFiles import LoadFiles
from InvalidArgumentException import InvalidArgumentException
from Button import Button
from TextBoxForQuestions import TextBoxForQuestions
import pygame
from unittest.mock import patch,Mock
import unittest

class MockRound(Round):
    def _create_interface(self):
        return "Abstact method implemented"

class TestRound(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.player = Player()
        self.round_singleplayer = MockRound(FIRST_ROUND_QUESTION_PATH,lambda : None,
                         POINTS_FOR_FIRST_ROUND,
                         TIME_FOR_FIRST_ROUND,
                         QUESTIONS_FOR_FIRST_ROUND,
                         self.player)
        self.player1 = Player()
        self.player2 = Player()
        self.round_multiplayer = MockRound(FIRST_ROUND_QUESTION_PATH,lambda : None,
                         POINTS_FOR_FIRST_ROUND,
                         TIME_FOR_FIRST_ROUND,
                         QUESTIONS_FOR_FIRST_ROUND,
                         self.player1,self.player2)
        self.loaded_data = LoadFiles.load_questions(FIRST_ROUND_QUESTION_PATH)

    def test_init(self):
        expected_attributes_for_singleplayer = {'loaded_data':self.loaded_data,
                                                'player' : self.player,
                                                'player_score' : None,
                                                'current_player' : self.player,
                                                'offset_upper_half':260,
                                                'offset':260,
                                                'answers':[],
                                                'buttons':[self.round_singleplayer.continue_button,self.round_singleplayer.go_back],
                                                'generated_questions':0,
                                                'points_for_round':POINTS_FOR_FIRST_ROUND,
                                                'time_for_round':TIME_FOR_FIRST_ROUND,
                                                'question_for_round':QUESTIONS_FOR_FIRST_ROUND}
        self.assertIsInstance(self.round_singleplayer.continue_button,Button)
        instance_attributes = vars(self.round_singleplayer)
        for attr_name, expected_value in expected_attributes_for_singleplayer.items():
            self.assertTrue(attr_name in instance_attributes)
            self.assertEqual(instance_attributes[attr_name], expected_value)
        expected_attributes_for_multiplayer = {'loaded_data':self.loaded_data,
                                                'player1' : self.player1,
                                                'player2' : self.player2,
                                                'player1_score' : None,
                                                'player2_score' : None,
                                                'current_player' : None,
                                                'offset_upper_half':260,
                                                'offset':260,
                                                'answers':[],
                                                'buttons':[self.round_multiplayer.continue_button,self.round_multiplayer.go_back],
                                                'generated_questions':0,
                                                'points_for_round':POINTS_FOR_FIRST_ROUND,
                                                'time_for_round':TIME_FOR_FIRST_ROUND,
                                                'question_for_round':QUESTIONS_FOR_FIRST_ROUND}
        self.assertIsInstance(self.round_multiplayer.continue_button,Button)   
        instance_attributes = vars(self.round_multiplayer)
        for attr_name, expected_value in expected_attributes_for_multiplayer.items():
            self.assertTrue(attr_name in instance_attributes)
            self.assertEqual(instance_attributes[attr_name], expected_value)

        with self.assertRaises(IndexError):
            self.round=MockRound(FIRST_ROUND_QUESTION_PATH,lambda : SecondRound(Player()),
                         POINTS_FOR_FIRST_ROUND,
                         TIME_FOR_FIRST_ROUND,
                         QUESTIONS_FOR_FIRST_ROUND,
                         Player(),Player(),Player())
            
    @patch('random.randrange')
    def test_choose_random_question(self,mock_choice):
        expected_result = { "question": "What is the capital of France?","choices": ["Berlin","Madrid","Paris","Rome"],"answer(s)": [ "Paris" ]}
        mock_choice.return_value = 0
        original_length = len(self.round_singleplayer.loaded_data)
        result = self.round_singleplayer._choose_random_question(self.round_singleplayer.loaded_data)
        self.assertEqual(result, expected_result)
        mock_choice.assert_called_with(original_length)

        self.round_singleplayer.loaded_data = [{"question": "Which planet is known as the Red Planet?","choices": ["Venus","Mars","Jupiter","Saturn"],"answer(s)": ["Mars"]}]
        expected_result = {"question": "Which planet is known as the Red Planet?","choices": ["Venus","Mars","Jupiter","Saturn"],"answer(s)": ["Mars"]}
        mock_choice.return_value = 0
        original_length = len(self.round_singleplayer.loaded_data)
        result = self.round_singleplayer._choose_random_question(self.round_singleplayer.loaded_data)
        self.assertEqual(result, expected_result)
        mock_choice.assert_called_with(original_length)

        with self.assertRaises(IndexError):
            result = self.round_singleplayer._choose_random_question([])

        with self.assertRaises(IndexError):
            result = self.round_singleplayer._choose_random_question(5)

    def test_is_correct(self):
        self.assertTrue(self.round_singleplayer._is_correct("The Rock", ["The Rock", "Dwayne johnson"]))
        self.assertFalse(self.round_singleplayer._is_correct("The Rocky",["The Rock", "Dwayne johnson"]))
        self.assertTrue(self.round_singleplayer._is_correct("the rock",["The Rock", "Dwayne johnson"]))
        self.assertFalse(self.round_singleplayer._is_correct("the rock",["Dwayne johnson"]))
        with self.assertRaises(InvalidArgumentException):
            self.round_singleplayer._is_correct(5,["The Rock", "Dwayne johnson"])
        with self.assertRaises(InvalidArgumentException):
            self.round_singleplayer._is_correct('the rock',"The Rock")
        with self.assertRaises(InvalidArgumentException):
            self.round_singleplayer._is_correct(5,"The Rock")
    
    def test_save_answer(self):
        self.random_question = self.round_singleplayer._choose_random_question(self.round_singleplayer.loaded_data)
        correct_answers = self.random_question["answer(s)"]
        self.round_singleplayer._save_answer(correct_answers)
        self.round_singleplayer.generated_questions+=1
        self.assertIsNot(self.round_singleplayer.answers,[])
        self.assertEqual(self.round_singleplayer.offset,260)
        self.assertIsInstance(self.round_singleplayer.answers[0],Button)
        self.random_question = self.round_singleplayer._choose_random_question(self.round_singleplayer.loaded_data)
        correct_answers = self.random_question["answer(s)"]
        self.round_singleplayer._save_answer(correct_answers)
        self.round_singleplayer.generated_questions += 1
        self.assertNotEqual(self.round_singleplayer.offset,260)
        for _ in range(5):
            self.random_question = self.round_singleplayer._choose_random_question(self.round_singleplayer.loaded_data)
            correct_answers = self.random_question["answer(s)"]
            self.round_singleplayer._save_answer(correct_answers)
            self.round_singleplayer.generated_questions+=1
        self.assertNotEqual(self.round_singleplayer.offset_upper_half,260)
        with self.assertRaises(InvalidArgumentException):
            self.round_singleplayer._save_answer(5)

    def test_render_intermediate_screen(self):
        self.round_singleplayer._render_intermediate_screen(self.round_singleplayer.screen)
        self.assertIsNot(self.round_singleplayer.player_score,None)
        self.assertIsInstance(self.round_singleplayer.player_score,Button)
        self.assertIn(self.round_singleplayer.player_score,self.round_singleplayer.buttons)
        answers = [Mock() for _ in range(len(self.round_singleplayer.answers))]
        self.round_singleplayer.answers = answers
        self.round_singleplayer._render_intermediate_screen(self.round_singleplayer.screen)
        for answer in answers:
            answer.draw.assert_called_once()
        with self.assertRaises(InvalidArgumentException):
            self.round_singleplayer._render_intermediate_screen([])

    def test_render_interface(self):
        screen = Mock(spec=pygame.surface.Surface)
        objects = [Mock() for _ in range(len(self.round_singleplayer.buttons))]
        self.round_singleplayer.objects = objects
        self.round_singleplayer.screen = screen
        self.round_singleplayer._render_interface(self.round_singleplayer.screen)
        for object in self.round_singleplayer.objects:
            object.draw.assert_called_once()
        screen.blit.assert_called_once_with(self.round_singleplayer.background, (0, 0))
        with self.assertRaises(InvalidArgumentException):
            self.round_singleplayer._render_intermediate_screen(5)

    def test_check_for_correct_answer(self):
        self.round_singleplayer.found_answer = True
        original_points = self.round_singleplayer.current_player.points
        self.assertTrue(self.round_singleplayer._check_for_correct_answer())
        self.assertEqual(original_points+self.round_singleplayer.points_for_round,self.round_singleplayer.current_player.points)
        self.round_singleplayer.found_answer = False
        original_points = self.round_singleplayer.current_player.points
        self.assertFalse(self.round_singleplayer._check_for_correct_answer())
        self.assertEqual(original_points,self.round_singleplayer.current_player.points)

    def test_handle_events(self):
        quit_event = pygame.event.Event(pygame.QUIT)
        self.assertEqual(TERMINATED,self.round_singleplayer._handle_events([quit_event]))
        pygame.init()
        skip_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        skip_event.button = 1
        self.round_singleplayer.skip_button = Button(screen_width//2-65,screen_height//2+125,150,50,f"Skip",lambda: None)
        skip_event.pos = self.round_singleplayer.skip_button.rect.topleft
        self.assertEqual(SKIPPED,self.round_singleplayer._handle_events([skip_event]))
        random_event = pygame.event.Event(pygame.ACTIVEEVENT)
        self.round_singleplayer.type_area = TextBoxForQuestions(screen_width // 2-115, screen_height // 2+84,250,35,lambda x,y: x+y,None)
        self.assertEqual(VALID,self.round_singleplayer._handle_events([random_event]))
        random_event_1 = pygame.event.Event(pygame.APP_DIDENTERFOREGROUND)
        random_event_2 = pygame.event.Event(pygame.CONTROLLER_AXIS_LEFTY)
        self.assertEqual(VALID,self.round_singleplayer._handle_events([random_event,random_event_1,random_event_2]))
        self.assertEqual(VALID,self.round_singleplayer._handle_events([]))
        self.assertEqual(None,self.round_singleplayer.found_answer)

    def test_render(self):
        self.round_singleplayer.generated_questions=self.round_singleplayer.question_for_round+1
        with patch('Singleplayer.Round.Round._render_intermediate_screen') as mock_choice:
            self.round_singleplayer.render(self.round_singleplayer.screen)
            mock_choice.assert_called_once()
            self.round_singleplayer.generated_questions=0
        with self.assertRaises(InvalidArgumentException):
            self.round_singleplayer.render(5)
    
    def test_abstract_method(self):
        self.assertEqual("Abstact method implemented",self.round_singleplayer._create_interface())

if __name__ == '__main__':
        unittest.main()