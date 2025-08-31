from rest_framework import serializers

class CommandSerializer(serializers.Serializer):
    command = serializers.CharField(max_length=1000)