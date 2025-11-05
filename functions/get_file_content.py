import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    wd_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(wd_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    try:

        file_size = os.path.getsize(target_path)

        with open(target_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)

            if file_size > MAX_CHARS:
                file_content_string += f'[...File {file_path} truncated at {MAX_CHARS} characters]'

            return file_content_string
        
    except Exception as e:
        return(f"Error reading file content: {e}")
    
# Schema for get_file_content function

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the contents of a file, truncated to 10000 characters. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to file for which to return contents, relative to the working directory. If file is not found, return an error message."
            )
        },
        required=["file_path"],
    )
)