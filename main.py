import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    verbose = '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]

    if not args:
        print('Error: prompt not provided')
        exit(1)

    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    user_prompt = ' '.join(args)

    if verbose:
        print(f'User prompt: {user_prompt}')

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

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

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes to files in the specified directory, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write to, relative to the working directory.",
                ),
                'string': types.Schema(
                    type=types.Type.STRING,
                    description='The text content to write to the file.',
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=config
    )

    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

    if not response.function_calls:
        print(f'Response: {response.text}')
    else:
        for part in response.function_calls:
            print(f'Calling function: {part.name}({part.args})')


if __name__ == '__main__':
    main()
