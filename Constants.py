from State import State
from FileCommands import FileCommands

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

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
TIME_FOR_SECOND_ROUND=1000
TIME_FOR_THIRD_ROUND=1000
TIME_FOR_FOURTH_ROUND=1000
TIME_FOR_FIFTH_ROUND=1000

QUESTIONS_FOR_FIRST_ROUND=10
QUESTIONS_FOR_SECOND_ROUND=10
QUESTIONS_FOR_THIRD_ROUND=10
QUESTIONS_FOR_FOURTH_ROUND=9
QUESTIONS_FOR_FIFTH_ROUND=5

TIME_FOR_LOADING_SCREEN=5000

FIRST_ROUND_QUESTION_PATH=FileCommands.find_file_path_in_current_directory('firstroundquestions.json')
SECOND_ROUND_QUESTION_PATH=FileCommands.find_file_path_in_current_directory('secondroundquestions.json')
THIRD_ROUND_QUESTION_PATH=FileCommands.find_file_path_in_current_directory('thirdroundquestions.json')
FOURTH_ROUND_QUESTION_PATH=FileCommands.find_file_path_in_current_directory('fourthroundquestions.json')
FIFTH_ROUND_QUESTION_PATH=FileCommands.find_file_path_in_current_directory('fifthroundquestions.json')
BACKGROUND_PATH = FileCommands.find_file_path_in_current_directory("background.png")

IMAGES_PATH=FileCommands.find_folder_path('images')
AUDIO_PATH=FileCommands.find_folder_path('audio-files')