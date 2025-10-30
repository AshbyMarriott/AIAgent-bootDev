import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    
    try:
        # get full absolute path to file given
        full_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_file_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # confirm file exists
        if not os.path.exists(full_file_path):
            return f'Error: File "{file_path}" not found.'
        
        # confirm file ends with '.py'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
    
        # run subprocess and return outputs
        completed_process = subprocess.run(['python', full_file_path] + args, capture_output=True, timeout=30, text=True, cwd=os.path.abspath(working_directory))
        if completed_process.stdout == '' and completed_process.stderr == '':
            return 'No output produced.'
        else:
            return (f"{f'STDOUT: {completed_process.stdout}' if completed_process.stdout else ''}"
            f"{f'STDERR: {completed_process.stderr}' if completed_process.stderr else ''}"
            f"{f'\nProcess exited with return code {completed_process.returncode}' if completed_process.returncode else ''}")
        
    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given python file as a subprocess with any arguments if given and prints the stdout and stderr outputs and any non-zero exit codes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING, description="Optional arguments to pass to the Python file."),
                description="A list of optional argument strings for the Python file being run."
            )
        },
    ),
)