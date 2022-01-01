from recipes.models import Rating, Recipe
from rest_framework import serializers


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['pk', 'user']



class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['pk', 'author', 'title', 'content', 'shortDescription', 'category', 'mainImage', 'view_count']

    def validate(self, data):
        return data

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)