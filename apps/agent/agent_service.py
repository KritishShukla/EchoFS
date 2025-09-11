from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from apps.tools.file_services import FileService
import re

class AgentService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0
        )
        self.file_service = FileService()
    
    def run_command(self, command):
        try:

            command_lower = command.lower()
            blocked_commands = [' cd ', ' mkdir', ' rmdir', ' rm ', ' mv ', ' cp ', ' chmod', ' chown', 
                              ' sudo', ' su ', ' exit', ' kill', ' ps ', ' ls ', ' pwd', ' whoami',
                              ' cat ', ' grep', ' find', ' which', ' export', ' source', ' bash']
            
            for blocked in blocked_commands:
                if blocked in f" {command_lower} ":
                    return f"Security: Command '{blocked.strip()}' is not allowed. Only file operations are permitted."
            

            prompt = f"""You are a file management assistant. Analyze this command and respond with ONLY the operation and parameters in this exact format:

OPERATION: [create_file|read_file|update_file|delete_file|list_files]
FILENAME: [filename if needed]
CONTENT: [actual code/content, not description]

Command: {command}

Examples:
- "Create a file called test.py with print hello" -> OPERATION: create_file, FILENAME: test.py, CONTENT: print("hello")
- "Create a python file to swap two numbers" -> OPERATION: create_file, FILENAME: swap.py, CONTENT: a = 5\nb = 10\na, b = b, a\nprint(f"a = {{a}}, b = {{b}}")
- "Read the config file" -> OPERATION: read_file, FILENAME: config
- "List all files" -> OPERATION: list_files
- "Delete old.txt" -> OPERATION: delete_file, FILENAME: old.txt
- "Update data.json with new info" -> OPERATION: update_file, FILENAME: data.json, CONTENT: {{"status": "updated"}}

IMPORTANT: For CONTENT, write actual code/data, not descriptions. Generate working code based on the request."""

            response = self.llm.invoke(prompt)
            

            response_text = response.content.strip()
            operation = None
            filename = None
            content = None
            
            if 'OPERATION:' in response_text:
                operation = response_text.split('OPERATION:')[1].split('\n')[0].strip()
            if 'FILENAME:' in response_text:
                filename = response_text.split('FILENAME:')[1].split('\n')[0].strip()
            if 'CONTENT:' in response_text:
                content_part = response_text.split('CONTENT:')[1].strip()
                content = content_part.replace('\\n', '\n')
            

            if operation == 'create_file' and filename and content:
                return self.file_service.create_file(filename, content)
            elif operation == 'read_file' and filename:
                return self.file_service.read_file(filename)
            elif operation == 'update_file' and filename and content:
                return self.file_service.update_file(filename, content)
            elif operation == 'delete_file' and filename:
                return self.file_service.delete_file(filename)
            elif operation == 'list_files':
                return self.file_service.list_files()
            else:
                return f"Could not understand command. Available operations: create, read, update, delete, list files."
            
        except Exception as e:
            return f"Error: {str(e)}"