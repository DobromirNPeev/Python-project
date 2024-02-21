from FileCommands import FileCommands
from Constants import IMAGES_PATH
import os
import shutil
import unittest

class FileCommandTest(unittest.TestCase):
    
    def test_find_file_path_in_current_directory(self):
        self.assertIsNone(FileCommands.find_file_path_in_current_directory('something.json'))
        found_path = FileCommands.find_file_path_in_current_directory('testfile.json')
        print(FileCommands.find_file_path_in_current_directory('download (11).jpg'))
        changed_path=''
        for character in found_path:
            if character == '\\':
                changed_path += '/'
                continue
            changed_path += character
        self.assertEqual('/Project/testfile.json',changed_path)
        self.assertIsNone(FileCommands.find_file_path_in_current_directory('420179369_780533263918099_7250403426819783222_n.jpg'))

    def test_finder_folder_path(self):
        self.assertEqual('D:\Project\images',FileCommands.find_folder_path('images'))
        self.assertIsNone(FileCommands.find_folder_path('random'))

    def test_move_file(self):
        FileCommands.move_file('D:/Project/testimage.jpg',IMAGES_PATH)
        file_path = os.path.join(IMAGES_PATH, 'testimage.jpg')
        self.assertTrue(os.path.exists(file_path) and os.path.isfile(file_path))
        FileCommands.move_file('D:/Project/images/testimage.jpg','D:/Project/')
        with self.assertRaises(shutil.Error):
            FileCommands.move_file('D:/Project/testimage.jpg','D:/Project/')

if __name__ == '__main__':
    unittest.main()