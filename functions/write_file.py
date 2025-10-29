import os

def write_file(working_directory, file_path, content):
    try:
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_file_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        dirname = os.path.dirname(full_file_path)
        if not os.path.exists(dirname):
            # print(f'Directory {dirname} does not exist. Creating...')
            os.makedirs(os.path.dirname(dirname))
        
        with open(full_file_path, "w") as f:
            chars_written = f.write(content)
            if chars_written == len(content):
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error:{e}'
