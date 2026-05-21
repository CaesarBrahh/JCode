import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    # convert working directory to an absolute path
    working_dir_abs = os.path.abspath(working_directory)

    # build requested target path
    file_path_rel = file_path
    file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path))

    # check if target is inside working directory
    valid_file_path = os.path.commonpath(
            [working_dir_abs, file_path]) == working_dir_abs
    if not valid_file_path:
        return f"Error: Cannot execute \"{file_path_rel}\" as it is outside the permitted working directory"

    # ensure file_path exists AND points to a file (not a dir)
    if not os.path.isfile(file_path):
        return f"Error: \"{file_path_rel}\" does not exist or is not a regular file"

    # ensure last 3 characters end in .py
    if file_path[-3:] != ".py":
        return f"Error: \"{file_path_rel}\" is not a Python file"

    # run subprocess to create CompletedProcess object
    command = ["python3", file_path]
    if args != None:
        command.extend(args)
    result = subprocess.run(
                command,
                cwd=working_dir_abs,
                capture_output=True,
                text=True,
                timeout=30

    )

    # build output string 
    output_string = ""
    if result.returncode != 0:
        output_string += f"Process exited with code {result.returncode}"
    if len(result.stdout) == 0 and len(result.stderr) == 0:
        output_string += f"\nNo output produced"
    else:
        if len(result.stdout) != 0:
            output_string += f"\nSTDOUT: {result.stdout}"
        if len(result.stderr) != 0:
            output_string += f"\nSTDERR: {result.stderr}"
    return output_string
