import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    # convert working directory to an absolute path
    working_dir_abs = os.path.abspath(working_directory)

    # build requested target path
    file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

    # check if target is inside working directory
    valid_file_path = os.path.commonpath(
            [working_dir_abs, file_path]) == working_dir_abs
    if not valid_file_path:
        return f"Error: Cannot read \"{file_path}\" as it is outside of the permitted working directory"

    # check whether file_path is a file
    if not os.path.isfile(file_path):
        return f"Error: File not found or is not a regular file: {file_path}"

    # read file
    with open(file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

        if f.read(1):
            file_content_string += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"

    return file_content_string

