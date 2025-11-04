import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_wd_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_wd_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ['python3', abs_file_path] + args
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=abs_wd_path)
        
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        
        if not result.stdout and not result.stderr:
            return "No output produced."
        
        return f"STDOUT:\n{result.stdout}\nSTDERR:{result.stderr}"
        
    except Exception as e:
        print(f"Error executing Python file: {e}")