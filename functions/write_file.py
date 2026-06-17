import os
from google.genai import types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        is_inside = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not is_inside:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if os.path.isdir(file_path_abs):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
        
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        if type(content) != str or content == "":
            raise Exception("invalid content")

        with open(file_path_abs, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'    
    except Exception as error:
        error_str = str(error)
        return f"Error: {error_str}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes new content with the given content argument on the file with the given file_path argument, returns a success string if the content was written successfully",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write on, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write with",
            ),
        },
    ),
)