import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory') 
        
        if not os.path.isdir(target_dir):
            raise Exception(f'"{directory}" is not a directory')
        # else:
        #     return f'Success: "{directory}" is within the working directory'

        entries_list = []
        for entry in os.scandir(target_dir):
            entry_str = f"{entry.name}: file_size={entry.stat().st_size}, is_dir={os.path.isdir(entry)}"
            entries_list.append(entry_str)

        return "\n- ".join(entries_list)
    except Exception as error:
        error_str = str(error)
        return f"Error: {error_str}"