import os
from google.genai import types

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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file content in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to list content from, relative to the working directory.",
            ),
        },
    ),
)
