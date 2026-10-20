import os
from config import MAX_CHARS
from .get_files_info import is_in_working_directory

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        full_path = os.path.join(working_directory, file_path)

        if not is_in_working_directory(working_directory, file_path):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

        if not os.path.isfile(full_path):
            return f"Error: File not found or is not a regular file \"{file_path}\""

        with open(full_path) as file:
            contents = file.read(MAX_CHARS)

            # Checks to see if file was larger than MAX_CHARS limit
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return contents

    except OSError as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of the specified file, up to 10,000 characters. The file must be in the working directory, and cannot be a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to retrieve contents from, relative to the working directory",
                },
            },
        },
    },
}
