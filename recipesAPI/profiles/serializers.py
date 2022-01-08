from rest_framework import serializers


class UserProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    rating = serializers.IntegerField(allow_null=True)
    views = serializers.IntegerField(allow_null=True)