from rest_framework import serializers
from recipesBackend.models import Rating, Message, Recipe




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

