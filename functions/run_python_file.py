import os
import subprocess


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
    
