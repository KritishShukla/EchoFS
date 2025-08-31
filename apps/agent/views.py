from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import CommandSerializer
from .agent_service import AgentService

@method_decorator(csrf_exempt, name='dispatch')
class CommandView(APIView):
    def post(self, request):
        serializer = CommandSerializer(data=request.data)
        if serializer.is_valid():
            command = serializer.validated_data['command']
            agent_service = AgentService()
            result = agent_service.run_command(command)
            return Response({'result': result})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)