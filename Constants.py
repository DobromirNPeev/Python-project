from State import State
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen_width, screen_height = 1000, 600

TERMINATED = State.TERMINATED
SKIPPED=State.SKIPPED
VALID=State.VALID

POINTS_FOR_FIRST_ROUND=1
POINTS_FOR_SECOND_ROUND=2
POINTS_FOR_THIRD_ROUND=3
POINTS_FOR_FOURTH_ROUND=4
POINTS_FOR_FIFTH_ROUND=5

TIME_FOR_FIRST_ROUND=30000
TIME_FOR_SECOND_ROUND=30000
TIME_FOR_THIRD_ROUND=30000
TIME_FOR_FOURTH_ROUND=30000
TIME_FOR_FIFTH_ROUND=90000

QUESTIONS_FOR_FIRST_ROUND=10
QUESTIONS_FOR_SECOND_ROUND=10
QUESTIONS_FOR_THIRD_ROUND=10
QUESTIONS_FOR_FOURTH_ROUND=9
QUESTIONS_FOR_FIFTH_ROUND=5

TIME_FOR_LOADING_SCREEN=5000

def find_file_path(filename):
    for root, dirs, files in os.walk('.'):
        if filename in files:
            return os.path.join(root, filename)
    return None

FIRST_ROUND_QUESTION_PATH=find_file_path('firstround.json')
SECOND_ROUND_QUESTION_PATH=find_file_path('questionsforimages.json')
THIRD_ROUND_QUESTION_PATH=find_file_path('audio-files.json')
FOURTH_ROUND_QUESTION_PATH=find_file_path('openquestions.json')
FIFTH_ROUND_QUESTION_PATH=find_file_path('hardquestions.json')