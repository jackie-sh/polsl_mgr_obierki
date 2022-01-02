from recipes.models import *
from rest_framework import serializers


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ['id', 'name']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'author', 'recipe', 'commentText', 'rating', 'create_date']


    def validate_rating(self, value):
        if value > 5 or value < 1:
            raise serializers.ValidationError("Rating out of scale 1-5")
        return value


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'author', 'title', 'content', 'shortDescription', 'category', 'mainImage', 'view_count', 'create_date', 'update_date']

    def validate(self, data):
        return data

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)


class RecipeFullViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'content', 'authorName', 'recipeId', 'authorId', 'createdDate', 'mainImageId', 'categoryId', 'rating', 'shortDescription', 'views', 'comments']


    #authorName