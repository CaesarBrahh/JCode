import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    # convert the working directory to an absolute path
    working_dir_abs = os.path.abspath(working_directory)

    # build requested target path
    target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory))

    # check if target is inside working directory
    valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs
    
    # error checking if target path not in working directory
    if not valid_target_dir:
        return f"Error: Cannot list \"{directory}\" as it is outside of the permitted working directory"

    # check whether target is truly a directory
    if not os.path.isdir(target_dir):
        return f"Error: \"{directory}\" is not a directory"

    # build string representing contents of the directory
    dir_items_str = ""
    for item in os.listdir(target_dir):
        full_path = os.path.join(target_dir, item)
        name = item
        size = os.path.getsize(full_path)
        is_dir = os.path.isdir(full_path)
        dir_items_str += f"- {name}: file_size={size} bytes, is_dir={is_dir}\n"
    return dir_items_str
    
