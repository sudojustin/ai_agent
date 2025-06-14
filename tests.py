import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_get_info_current_dir(self):
        result = get_files_info('calculator', '.')
        print('Result for current directory:')
        print(f'{result}\n')

    def test_get_info_pkg(self):
        result = get_files_info('calculator', 'pkg')
        print('Result for "pkg" directory:')
        print(f'{result}\n')

    def test_get_info_bin(self):
        result = get_files_info('calculator', '/bin')
        print('Result for "/bin" directory:')
        print(f'{result}\n')

    def test_get_info_parent(self):
        result = get_files_info('calculator', '../')
        print('Result for "../" directory:')
        print(f'{result}\n')


if __name__ == '__main__':
    unittest.main()
