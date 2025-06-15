import os
import sys
import subprocess
from google.genai import types

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


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, relative to the working directory.",
            ),
        },
    ),
)
