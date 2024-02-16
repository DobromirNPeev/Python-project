import unittest
from SaveFiles import SaveFiles
from LoadFiles import LoadFiles
from Constants import FOURTH_ROUND_QUESTION_PATH
import pygame
from AddQuestionScreen import AddQuestionScreen

class SaveFilesTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.loaded_data=LoadFiles.load_questions(FOURTH_ROUND_QUESTION_PATH)

    def test_save_data(self):
        self.data={"question": "something",
                   "answer(s)": ['answer'],
                   "needed_answers": 8}
        result=SaveFiles.save_data(self.data,self.loaded_data,'testfile.json')
        self.assertIsInstance(result,AddQuestionScreen)
        self.loaded_data_test=LoadFiles.load_questions('testfile.json')
        self.assertEqual(self.loaded_data,self.loaded_data_test)
        self.data={"question": "something",
                   "answer(s)": [],
                   "needed_answers": 8}       
        result=SaveFiles.save_data(self.data,self.loaded_data,'testfile.json')
        self.assertIsInstance(result,AddQuestionScreen)


if __name__=='__main__':
    unittest.main()