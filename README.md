EchoFS - Django LangChain Agent

AI-powered file management system using Django, LangChain, and Google's Gemini models.

Setup

1. Install dependencies:
pip install -r requirements.txt

2. Set your Gemini API key in .env:
GEMINI_API_KEY=your_actual_api_key_here

3. Start the server:
python manage.py runserver

Usage

Send POST requests to /api/agent/command/ with:
{
  "command": "Create a file called hello.txt with content 'Hello World'"
}

The agent will interpret natural language commands and execute file operations in the sandboxed workspace/ directory.

Available Commands

- Create files with content
- Read file contents  
- List files in directories

All operations are restricted to the workspace/ directory for security.