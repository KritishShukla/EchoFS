from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from apps.tools.file_services import FileService
import re

class AgentService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.GEMINI_API_KEY
        )
        self.file_service = FileService()
    
    def run_command(self, command):
        try:
            # Security checks - block dangerous commands
            command_lower = command.lower()
            
            # Block directory navigation and system commands
            blocked_commands = ['cd ', 'mkdir', 'rmdir', 'rm ', 'mv ', 'cp ', 'chmod', 'chown', 
                              'sudo', 'su ', 'exit', 'kill', 'ps ', 'ls ', 'pwd', 'whoami',
                              'cat ', 'grep', 'find', 'which', 'export', 'source', 'bash']
            
            for blocked in blocked_commands:
                if blocked in command_lower:
                    return f"Security: Command '{blocked.strip()}' is not allowed. Only file operations are permitted."
            
            # Simple command parsing for file operations
            command = command_lower
            
            if "create" in command and "file" in command:
                # Extract filename and content
                if "with content" in command:
                    parts = command.split("with content")
                    filename = re.search(r"create.*?file.*?called\s+([\w\.]+)", parts[0])
                    if filename:
                        content = parts[1].strip().strip("'\"")
                        return self.file_service.create_file(filename.group(1), content)
            
            elif "read" in command and "file" in command:
                filename = re.search(r"read.*?file.*?([\w\.]+)", command)
                if filename:
                    return self.file_service.read_file(filename.group(1))
            
            elif "list" in command and "file" in command:
                return self.file_service.list_files()
            
            elif "delete" in command and "file" in command:
                filename = re.search(r"delete.*?file.*?([\w\.]+)", command)
                if filename:
                    return self.file_service.delete_file(filename.group(1))
            
            return "I can help you create files, read files, list files, or delete files. Try: 'Create a file called test.txt with content Hello World'"
            
        except Exception as e:
            return f"Error: {str(e)}"