from rest_framework import serializers
from przepisy_backend.models import User, Rating, Message, Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'login', 'password', 'email')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'comments', 'rating', 'pub_date', 'user')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'pub_date', 'sender', 'receiver')


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'description', 'recipe_type', 'views', 'rating', 'file')

