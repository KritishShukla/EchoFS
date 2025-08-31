from langchain.tools import Tool
from .file_services import FileService

def get_tools():
    return [
        Tool(
            name="create_file",
            description="Create a new file with specified content. Args: file_path (str), content (str)",
            func=lambda args: FileService.create_file(*args.split('|', 1))
        ),
        Tool(
            name="read_file", 
            description="Read the contents of a file. Args: file_path (str)",
            func=FileService.read_file
        ),
        Tool(
            name="list_files",
            description="List all files in a directory. Args: directory_path (str, optional)",
            func=FileService.list_files
        )
    ]