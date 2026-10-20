import os
from .get_files_info import is_in_working_directory

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        full_path = os.path.join(working_directory, file_path)

        if not is_in_working_directory(working_directory, file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(full_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(full_path, mode = "w") as file:
            file.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrites the contents of the specified file with the passed string. File must be a regular file, and must be within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The string that will overwrite the specified file's contents",
                },
            },
        },
    },
}
