import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        is_inside = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not is_inside:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(file_path_abs):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        
        with open(file_path_abs, "r") as file:
            file_content_str = file.read(MAX_CHARS)

            if file.read(1):
                file_content_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_str
    except Exception as error:
        error_str = str(error)
        return f"Error: {error_str}"