import os
from config import MAX_CHARACTERS


def get_file_content(working_directory, file_path):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        full_working_directory = os.path.abspath(working_directory)

        if not full_file_path.startswith(full_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS)
            if not f.read(1) == '':
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error:{e}"