from rest_framework import serializers
from recipesBackend.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message', 'pub_date', 'sender', 'receiver']


