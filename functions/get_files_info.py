import os

def get_files_info(working_directory, directory="."):
    try:
        # get full absolute path to specified directory
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        # get absolute path to working directory
        working_full_path = os.path.abspath(working_directory)

        #print(f"Getting abspath of the join of {working_directory} and {directory} = {full_path}")
        if not full_path.startswith(working_full_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        files_info = ''
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)
            files_info += f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"
        return files_info
    except Exception as e:
        return f"Error:{e}"
