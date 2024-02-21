import unittest
from OpenFiles import OpenFiles
from FileCommands import FileCommands

class OpenFilesTest(unittest.TestCase):

    #only in the same directory
    def test_open_audio(self):
        image,basepath,path = OpenFiles.open_image()
        found_path = FileCommands.find_file_path_in_current_directory(basepath)
        changed_path = ''
        print(found_path)
        for character in found_path:
            if character == '\\':
                changed_path += '/'
                continue
            changed_path +=character
        self.assertEqual(path[2:],changed_path)

if __name__ == '__main__':
    unittest.main()