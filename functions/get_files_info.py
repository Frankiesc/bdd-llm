import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(working_dir_abs, directory))

        if not is_in_working_directory(working_directory, directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_items = []
        for item in os.listdir(target_dir):
            element_path = os.path.join(target_dir, item)
            element_size = os.path.getsize(element_path)
            is_dir = os.path.isdir(element_path)
            dir_items.append(format_file_info(item, element_size, is_dir))

        return "\n".join(dir_items)
    except Exception as e:
        return f"Error: {str(e)}"

def format_file_info(file_name: str, file_size: int, is_dir: bool) -> str:
    return f"- {file_name}: file_size={file_size}, is_dir={is_dir}"

def is_in_working_directory(working_directory: str, directory: str = ".") -> bool:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_dir_abs, directory))
    return os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
