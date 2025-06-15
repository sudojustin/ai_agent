import os
from google.genai import types

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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)




