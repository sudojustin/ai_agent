import unittest
from functions.get_files_info import get_files_info, get_file_content

class TestGetFilesInfo(unittest.TestCase):
    # def test_get_info_current_dir(self):
    #     result = get_files_info('calculator', '.')
    #     print('Result for current directory:')
    #     print(f'{result}\n')
    #
    # def test_get_info_pkg(self):
    #     result = get_files_info('calculator', 'pkg')
    #     print('Result for "pkg" directory:')
    #     print(f'{result}\n')
    #
    # def test_get_info_bin(self):
    #     result = get_files_info('calculator', '/bin')
    #     print('Result for "/bin" directory:')
    #     print(f'{result}\n')
    #
    # def test_get_info_parent(self):
    #     result = get_files_info('calculator', '../')
    #     print('Result for "../" directory:')
    #     print(f'{result}\n')

    def test_get_file_content_main(self):
        result = get_file_content('calculator', 'main.py')
        print(result)

    def test_get_file_content_pkg(self):
        result = get_file_content('calculator', 'pkg/calculator.py')
        print(result)

    def test_get_file_content_bin(self):
        result = get_file_content('calculator', '/bin/cat')
        print(result)


if __name__ == '__main__':
    unittest.main()
