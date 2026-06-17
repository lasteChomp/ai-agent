import os
import subprocess
from google.genai import types


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        is_inside = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not is_inside:
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(file_path_abs):
            raise Exception(f'"{file_path}" does not exist or is not a regular file')
        
        if os.path.basename(file_path_abs)[-3:] != ".py":
            raise Exception(f'"{file_path}" is not a Python file')
        
        command = ["python3", file_path_abs]

        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output = ""

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        
        if not result.stdout and not result.stderr:
            output += "No output produced"
        
        if result.stdout:
            output += f"STDOUT: {result.stdout}"

        if result.stderr:
            output += f"STDERR: {result.stderr}"

        return output
    except Exception as error:
        error_str = str(error)
        return f"Error: executing Python file: {error_str}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""
    Returns an output that was assigned to the stdout of a CompletedProcess object of a python file.

    If the returncode is not 0, adds this string to the output: Process exited with code <returncode>.

    If both the stdout and stderr don't exist, adds this string to the output: No output produced.

    If the stderr exists, adds stderr to the output.
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description= "Python file path to run the python file from, relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The list of the optional arguments to be added to the command that will be run",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="The optional argument of the command that will be run",
                ),
            ),
        },
    ),
)