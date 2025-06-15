import unittest
from functions.get_files_info import run_python_file

class TestGetFilesInfo(unittest.TestCase):
    def test_run_python_file_main(self):
        result = run_python_file('calculator', 'main.py')
        print(result)

    def test_run_python_file_tests(self):
        result = run_python_file('calculator', 'tests.py')
        print(result)

    def test_run_python_file_parent(self):
        result = run_python_file('calculator', '../main.py')
        print(result)

    def test_run_python_file_fail(self):
        result = run_python_file('calculator', 'nonexistent.py')
        print(result)


if __name__ == '__main__':
    unittest.main()
