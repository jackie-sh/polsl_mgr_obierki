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


class RatingRecipeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'author', 'recipe', 'commentText', 'rating', 'create_date']

class RecipeFullViewSerializer(serializers.ModelSerializer):
    recipeId = serializers.IntegerField(source='id')
    views = serializers.IntegerField(source='view_count')
    createdDate = serializers.DateTimeField(source='create_date')
    comments = serializers.SerializerMethodField()
    mainImageId = serializers.SerializerMethodField()
    categoryId = serializers.SerializerMethodField()

    authorName = serializers.SerializerMethodField()
    authorId = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['authorName', 'authorId', 'recipeId', 'title', 'content', 'categoryId',
                  'shortDescription',
                  'createdDate', 'mainImageId', 'views', 'rating', 'comments']

    def get_comments(self, obj):
        comments = Rating.objects.filter(recipe =obj.id)
        return RatingRecipeGetSerializer(comments, many=True).data

    def get_categoryId(self, obj):
        return obj.category.id

    def get_mainImageId(self, obj):
        if obj.mainImage:
            return obj.mainImage.id
        return obj.mainImage

    def get_authorName(self, obj):
        return obj.author.name

    def get_authorId(self, obj):
        return obj.author.id

    def get_rating(self,obj):
        comments = Rating.objects.filter(recipe=obj.id)
        return 0