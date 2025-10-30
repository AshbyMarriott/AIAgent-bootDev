import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_file_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        dirname = os.path.dirname(full_file_path)
        if not os.path.exists(dirname):
            print(f'Directory {dirname} does not exist. Creating...')
            os.makedirs(dirname, exist_ok=True)
        
        with open(full_file_path, "w") as f:
            chars_written = f.write(content)
            if chars_written == len(content):
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error:{e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates the given directory and file if not already existing relative to the working directory. If the file already exists, overwrites the given content to the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string of content to write to the specified file."
            )
        },
    ),
)