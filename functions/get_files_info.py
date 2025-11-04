import os

def get_files_info(working_directory, directory="."):

    try:

        results = f"Result for '{directory}' directory:"
        new_directory = directory
        # list contents of the working directory
        wd_contents = os.listdir(working_directory)
        
        # if the directory is not in the working directory...
        if directory not in wd_contents and directory != ".":
            error = f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
            results = results + "\n" + error
            print(results)
            return error
        
        # if no directory is provided, the working directory is the full path
        if directory == ".":
            new_directory = ""

        full_path = os.path.join(working_directory, new_directory)
        abs_full_path = os.path.abspath(full_path)
        is_valid_directory = os.path.isdir(abs_full_path)

        if not is_valid_directory:
            error = f'    Error: "{directory}" is not a directory'
            results += "\n" + error
            print(results)
            return error

        # if we made it this far, then we are working with a directory
        current_dir_contents = os.listdir(abs_full_path)

        filtered_contents = [item for item in current_dir_contents if item != "__pycache__"]

        
        for item in filtered_contents:
            path_to_item = os.path.join(abs_full_path, item)
            results += "\n" + f" - {item}: file_size:{os.path.getsize(path_to_item)} bytes, is_dir={os.path.isdir(path_to_item)}"
            
        print(results)    
        return results
    
    except Exception as e:
        print(f"Error: {e}")