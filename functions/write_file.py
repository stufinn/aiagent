import os
from google.genai import types

def write_file(working_directory, file_path, content):
    wd_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(wd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        try:

            # get the directory name for the target file
            dir_name = os.path.dirname(target_path)
            
            # check if directory exists already
            dir_name_exists = os.path.exists(dir_name)

            # if directory does not yet exist, create it
            if not dir_name_exists:
                os.makedirs(dir_name, exist_ok=True)

        except Exception as e:
            return f"Error creating directory: {e}"
    
    # Exit with error if the file_path is a directory and not a file    
    if os.path.exists(target_path) and os.path.isdir(target_path):
        return f"Error: {file_path} is a directory, not a file."
        
    try:
        # create a new file at target path
        with open(target_path, "w") as file:
                file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        print(f"Error writing to file: {e}")


# schema for write_file function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Updates files with new content or creates a new file, within the working directory only.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to file."
            )
        },
        required=["file_path", "content"],
    )
)