from recipes.models import Rating, Recipe
from rest_framework import serializers

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'comments', 'rating', 'pub_date', 'user')

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'description', 'recipe_type', 'view_count', 'rating', 'file')

