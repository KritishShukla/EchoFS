#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.insert(0, '/Users/kritishshukla/Documents/kritish/projects/EchoFS')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_gemini_agent.settings')
django.setup()

# Test the agent service directly
from apps.agent.agent_service import AgentService

try:
    agent = AgentService()
    result = agent.run_command("Create a file called test.txt with content Hello World")
    print("SUCCESS:", result)
except Exception as e:
    print("ERROR:", str(e))
    import traceback
    traceback.print_exc()