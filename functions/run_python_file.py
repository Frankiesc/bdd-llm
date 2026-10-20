import os
import subprocess
from .get_files_info import is_in_working_directory

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not is_in_working_directory(working_directory, file_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_path]

        # If additional arguments were passed, append to command
        if args:
            command.extend(args)

        abs_working_directory = os.path.abspath(working_directory)
        completed_process = subprocess.run(command, cwd=abs_working_directory, capture_output=True, timeout=30.0, text=True)

        output_string = ""

        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}\n"

        if not completed_process.stderr and not completed_process.stdout:
            output_string += "No output produced\n"
        if completed_process.stdout:
                output_string += f"STDOUT: {completed_process.stdout}\n"
        if completed_process.stderr:
            output_string += f"STDERR: {completed_process.stderr}\n"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes the file passed as the first argument and outputs stdout and stderr if present. Additional arguments are passed as parameters for the Python file. File must be a Python file within the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to be executed, relative to the working directory",
                },
                "args" : {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to be passed to the python file parameters"
                }
            },
        },
    },
}
