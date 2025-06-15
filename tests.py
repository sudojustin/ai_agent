import unittest
from functions.get_files_info import write_file

class TestGetFilesInfo(unittest.TestCase):
    def test_write_file_lorem(self):
        result = write_file('calculator', 'lorem.txt', 'wait, this isn\'t lorem ipsum')
        print(result)

    def test_write_file_pkg(self):
        result = write_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet')
        print(result)

    def test_write_file_tmp(self):
        result = write_file('calculator', '/tmp/temp.txt', 'this should not be allowed')
        print(result)

if __name__ == '__main__':
    unittest.main()
