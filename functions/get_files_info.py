import os

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
