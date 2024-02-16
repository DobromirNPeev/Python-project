import unittest
import pygame
from Constants import FIRST_ROUND_QUESTION_PATH,IMAGES_PATH,SECOND_ROUND_QUESTION_PATH,THIRD_ROUND_QUESTION_PATH,AUDIO_PATH
from LoadFiles import LoadFiles
from InvalidArgumentException import InvalidArgumentException
import pydub

class LoadFilesTests(unittest.TestCase):
    
    def test_load_questions(self):
        with self.assertRaises(InvalidArgumentException):
            LoadFiles.load_questions('erkjl')
        with self.assertRaises(InvalidArgumentException):
            LoadFiles.load_questions(56)
        with self.assertRaises(ValueError):
            LoadFiles.load_questions('D:/Project/FourthRoundMultiplayer.py')
        loaded_files=LoadFiles.load_questions(FIRST_ROUND_QUESTION_PATH)
        self.assertEqual(loaded_files,[
                                    {
                                    "question": "What is the capital of France?",
                                    "choices": [
                                        "Berlin",
                                        "Madrid",
                                        "Paris",
                                        "Rome"
                                    ],
                                    "answer(s)": [
                                        "Paris"
                                    ]
                                    },
                                    {
                                    "question": "Which planet is known as the Red Planet?",
                                    "choices": [
                                        "Venus",
                                        "Mars",
                                        "Jupiter",
                                        "Saturn"
                                    ],
                                    "answer(s)": [
                                        "Mars"
                                    ]
                                    },
                                    {
                                    "question": "What is the largest ocean on Earth?",
                                    "choices": [
                                        "Atlantic",
                                        "Indian",
                                        "Arctic",
                                        "Pacific"
                                    ],
                                    "answer(s)": [
                                        "Pacific"
                                    ]
                                    },
                                    {
                                    "question": "Who wrote the play 'Romeo and Juliet'?",
                                    "choices": [
                                        "Charles Dickens",
                                        "William Shakespeare",
                                        "Jane Austen",
                                        "Emily Bronte"
                                    ],
                                    "answer(s)": [
                                        "William Shakespeare"
                                    ]
                                    },
                                    {
                                    "question": "Which element has the chemical symbol 'O'?",
                                    "choices": [
                                        "Oxygen",
                                        "Osmium",
                                        "Oganesson",
                                        "Osmium"
                                    ],
                                    "answer(s)": [
                                        "Oxygen"
                                    ]
                                    },
                                    {
                                    "question": "In which year did the United States declare its independence?",
                                    "choices": [
                                        "1776",
                                        "1789",
                                        "1801",
                                        "1756"
                                    ],
                                    "answer(s)": [
                                        "1776"
                                    ]
                                    },
                                    {
                                    "question": "What is the currency of Japan?",
                                    "choices": [
                                        "Won",
                                        "Yuan",
                                        "Yen",
                                        "Ringgit"
                                    ],
                                    "answer(s)": [
                                        "Yen"
                                    ]
                                    },
                                    {
                                    "question": "Which famous scientist developed the theory of general relativity?",
                                    "choices": [
                                        "Isaac Newton",
                                        "Albert Einstein",
                                        "Galileo Galilei",
                                        "Stephen Hawking"
                                    ],
                                    "answer(s)": [
                                        "Albert Einstein"
                                    ]
                                    },
                                    {
                                    "question": "What is the capital of Australia?",
                                    "choices": [
                                        "Sydney",
                                        "Melbourne",
                                        "Canberra",
                                        "Brisbane"
                                    ],
                                    "answer(s)": [
                                        "Canberra"
                                    ]
                                    },
                                    {
                                    "question": "Which gas makes up the majority of Earth's atmosphere?",
                                    "choices": [
                                        "Oxygen",
                                        "Carbon Dioxide",
                                        "Nitrogen",
                                        "Argon"
                                    ],
                                    "answer(s)": [
                                        "Nitrogen"
                                    ]
                                    },
                                    {
                                    "question": "Who painted the Mona Lisa?",
                                    "choices": [
                                        "Vincent van Gogh",
                                        "Pablo Picasso",
                                        "Leonardo da Vinci",
                                        "Claude Monet"
                                    ],
                                    "answer(s)": [
                                        "Leonardo da Vinci"
                                    ]
                                    },
                                    {
                                    "question": "What is the largest mammal in the world?",
                                    "choices": [
                                        "Elephant",
                                        "Blue Whale",
                                        "Giraffe",
                                        "Hippopotamus"
                                    ],
                                    "answer(s)": [
                                        "Blue Whale"
                                    ]
                                    }
                                ])
        with open('empty_file.json', 'w') as f:
            f.write('{}')
        loaded_data = LoadFiles.load_questions('empty_file.json')
        self.assertEqual(loaded_data, {})
    
    def test_load_multimedia_images(self):
        loaded_data = LoadFiles.load_questions(SECOND_ROUND_QUESTION_PATH)
        multimedia_data = LoadFiles._LoadFiles__load_multimedia_data(loaded_data,IMAGES_PATH, 'something')
        self.assertEqual([],multimedia_data)
        multimedia_data = LoadFiles._LoadFiles__load_multimedia_data(loaded_data,IMAGES_PATH, 'images')
        with self.assertRaises(BaseException):
            LoadFiles._LoadFiles__load_multimedia_data('random',IMAGES_PATH, 'images')
        with self.assertRaises(BaseException):
            LoadFiles._LoadFiles__load_multimedia_data({'question':5,'random':9,'answer(s)':8},IMAGES_PATH, 'images')
        with self.assertRaises(BaseException):
            LoadFiles._LoadFiles__load_multimedia_data({'question':5,'random':9,'answer(s)':8},'random', 'images')
        self.questions=[]
        self.answers=[]
        for entry in loaded_data:
            self.questions.append(entry['question'])
            self.answers.append(entry['answer(s)'])
        multimedia_data=LoadFiles._LoadFiles__load_multimedia_data(loaded_data,IMAGES_PATH, 'images')
        for element in multimedia_data:
            self.assertIn(element['question'],self.questions)
            self.assertIsInstance(element['image'],pygame.Surface)
            self.assertIsInstance(element['rect'],pygame.Rect)
            self.assertIn(element['answer(s)'],self.answers)
        loaded_data = LoadFiles.load_questions(THIRD_ROUND_QUESTION_PATH)
        self.questions=[]
        self.answers=[]
        for entry in loaded_data:
            self.questions.append(entry['question'])
            self.answers.append(entry['answer(s)'])
        multimedia_data=LoadFiles._LoadFiles__load_multimedia_data(loaded_data,AUDIO_PATH, 'audio-files')
        for element in multimedia_data:
            self.assertIn(element['question'],self.questions)
            self.assertIsInstance(element['audio'],pydub.AudioSegment)
            self.assertIn(element['answer(s)'],self.answers)


if __name__=='__main__':
    unittest.main()