from langchain.tools import Tool
from .file_services import FileService

def create_file_tool(input_str):
    parts = input_str.split('|', 1)
    if len(parts) != 2:
        return "Error: Please provide file_path|content"
    return FileService.create_file(parts[0].strip(), parts[1].strip())

def update_file_tool(input_str):
    parts = input_str.split('|', 1)
    if len(parts) != 2:
        return "Error: Please provide file_path|content"
    return FileService.update_file(parts[0].strip(), parts[1].strip())

def get_tools():
    return [
        Tool(
            name="create_file",
            description="Create a new file with content. Input format: 'filename.txt|file content here'",
            func=create_file_tool
        ),
        Tool(
            name="read_file", 
            description="Read the contents of a file. Input: filename.txt",
            func=FileService.read_file
        ),
        Tool(
            name="update_file",
            description="Update existing file with new content. Input format: 'filename.txt|new content here'",
            func=update_file_tool
        ),
        Tool(
            name="delete_file",
            description="Delete a file. Input: filename.txt",
            func=FileService.delete_file
        ),
        Tool(
            name="list_files",
            description="List all files in workspace directory. Input: (leave empty or directory path)",
            func=lambda x: FileService.list_files(x if x else "")
        )
    ]