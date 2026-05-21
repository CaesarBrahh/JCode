import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    # convert working directory to an absolute path
    working_dir_abs = os.path.abspath(working_directory)

    # build requested target path
    file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

    # check if target is inside working directory
    valid_file_path = os.path.commonpath(
            [working_dir_abs, file_path]) == working_dir_abs
    if not valid_file_path:
        return f"Error: Cannot write to \"{file_path}\" as it is outside of the permitted working directory"

    # check whether file_path points to an existing directory
    if os.path.isdir(file_path):
        return f"Error: Cannot write to \"{file_path}\" as it is a directory"

    # create directories if doesn't exist
    parent_directory = os.path.dirname(file_path)
    os.makedirs(parent_directory, exist_ok=True)

    # open and write to file
    with open(file_path, "w") as f:
        f.write(content)
    return f"Successfully wrote to \"{file_path}\". {len(content)} characters written"
