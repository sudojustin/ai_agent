import os
import sys
import subprocess

def get_files_info(working_directory, directory=None):
    try:
        working_directory = os.path.abspath(working_directory)
        if directory is None:
            directory = working_directory
        else:
            directory = os.path.abspath(os.path.join(working_directory, directory))

        if not directory.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            try:
                size = os.path.getsize(full_path)
                is_dir = os.path.isdir(full_path)
                entries.append(f'- {entry}: file_size={size}, is_dir={is_dir}')
            except Exception as e:
                entries.append(f'- {entry}: Error reading file info: {e}')

        return '\n'.join(entries)

    except Exception as e:
        return f'Error: {e}'


def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f'Error: {e}'

    if len(file_content_string) > 10000:
        return file_content_string + ' truncated at 10000 characters'
    return file_content_string


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f'Error: creating directory: {e}'

    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: {file_path} is a directory, not a file'

    try:
        with open(abs_file_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            [sys.executable, abs_file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
    )
    except Exception as e:
        return f'Error: executing Python file: {e}'

    print(f'STDOUT: {result.stdout}')
    print(f'STDERR: {result.stderr}')

    if result.returncode != 0:
        print(f'Process exited with code {result.returncode}')
    if not result.stdout and not result.stderr:
        return f'No output produced.'

