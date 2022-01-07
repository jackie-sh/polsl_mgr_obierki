import logging

from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser
from .models import Recipe, RecipeCategory, RecipeImage, Rating
from .serializers import *
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from rest_framework import status


def get_all(request):
    recipes = Recipe.objects.all()
    data = serializers.serialize('json', recipes)
    return HttpResponse(data, content_type='application/json')


class RecipeCreateComment(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecipeCategorySerializer

    @swagger_auto_schema(tags=["recipe"],
                         request_body=Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 'recipeId': Schema(type=TYPE_STRING),
                                 'commentText': Schema(type=TYPE_STRING),
                                 'rating': Schema(type=TYPE_INTEGER)
                             }
                         ),
                         responses={
                             status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                                        properties={'isCreated': Schema(type=TYPE_BOOLEAN)}
                                                        )
                         }
                         )
    def post(self, request):
        data = request.data
        data['recipe'] = data['recipeId']
        data['author'] = request.user.id
        serializer = RecipeCategorySerializer(data=data)
        return create_response(serializer)


def create_response(serializer):
    if serializer.is_valid():
        serializer.save()
        data = {'isCreated': True, 'id': serializer.data.get('id')}
        return JsonResponse(data, status=status.HTTP_201_CREATED)

    data = {'isCreated': False, 'errorMessage': serializer.errors}
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class RecipeUploadImage(GenericAPIView):
    serializer_class = RecipeImageSerializer
    parser_class = [FileUploadParser]

    @swagger_auto_schema(tags=["image"],
                         request_body=Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 'recipeId': Schema(type=TYPE_INTEGER),
                                 'file': Schema(type=TYPE_STRING),
                             }
                         ),
                         responses={
                             status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                                        properties={
                                                            'isCreated': Schema(type=TYPE_BOOLEAN),
                                                            'mainImageId': Schema(type=TYPE_INTEGER),
                                                        })
                         }
                         )
    def post(self, request):
        serializer = RecipeImageSerializer(data=request.data)
        return create_response(serializer)


class RecipeGetImage(GenericAPIView):
    serializer_class = RecipeImageSerializer

    @swagger_auto_schema(tags=["image"],
                         responses={
                             status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                                        properties={
                                                            'mainImageId': Schema(type=TYPE_INTEGER),
                                                            'file': Schema(type=TYPE_STRING),
                                                        })
                         }
                         )
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            recipeImageId = recipe.mainImage.id
            recipeImage = RecipeImage.objects.get(pk=recipeImageId)
        except Recipe.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        recipeImageSerializer = RecipeImageSerializer(recipeImage)
        return JsonResponse(recipeImageSerializer.data, safe=False, status=status.HTTP_200_OK)


class RecipeGetView(GenericAPIView):
    serializer_class = RecipeSerializer

    @swagger_auto_schema(tags=["recipe"],
                         responses={
                             status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                                        properties={
                                                            'title': Schema(type=TYPE_STRING),
                                                            'content': Schema(type=TYPE_STRING),
                                                            'authorName': Schema(type=TYPE_STRING),
                                                            'recipeId': Schema(type=TYPE_INTEGER),
                                                            'authorId': Schema(type=TYPE_INTEGER),
                                                            'mainImageId': Schema(type=TYPE_INTEGER),
                                                            'categoryId': Schema(type=TYPE_INTEGER),
                                                            'shortDescription': Schema(type=TYPE_STRING),
                                                        })
                         }
                         )
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        recipe_serializer = RecipeSerializer(recipe, data={'view_count': recipe.view_count + 1}, partial=True)
        try:
            if recipe_serializer.is_valid(raise_exception=True):
                recipe_serializer.save()
                recipe = Recipe.objects.get(pk=pk)
                serializer_view = RecipeFullViewSerializer(recipe)
                return JsonResponse(serializer_view.data, safe=False, status=status.HTTP_200_OK)
        except serializers.ValidationError as valEr:
            return JsonResponse({'errorMessage': valEr.detail}, status=status.HTTP_400_BAD_REQUEST)


class RecipeCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecipeSerializer

    @swagger_auto_schema(tags=["recipe"],
                         request_body=Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 'title': Schema(type=TYPE_STRING),
                                 'content': Schema(type=TYPE_STRING),
                                 'categoryId': Schema(type=TYPE_INTEGER),
                                 'shortDescription': Schema(type=TYPE_STRING),
                                 'mainImageId': Schema(type=TYPE_INTEGER)
                             }
                         ),
                         responses={
                             status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                                        properties={'isCreated': Schema(type=TYPE_BOOLEAN),
                                                                    'id': Schema(type=TYPE_INTEGER)}
                                                        )
                         }
                         )
    def post(self, request):
        data = request.data
        data['category'] = data['categoryId']
        data['author'] = request.user.id
        data['view_count'] = 0
        data['mainImage'] = data['mainImageId']
        serializer = RecipeSerializer(data=data)
        return create_response(serializer)


class RecipeEditView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecipeSerializer

    @swagger_auto_schema(tags=["recipe"],
                         request_body=Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 'title': Schema(type=TYPE_STRING),
                                 'content': Schema(type=TYPE_STRING),
                                 'categoryId': Schema(type=TYPE_INTEGER),
                                 'shortDescription': Schema(type=TYPE_STRING),
                                 'mainImageId': Schema(type=TYPE_INTEGER)
                             }
                         ))
    def put(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return JsonResponse({'isUpdated': False, 'errorMessage': "Recipe does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)

        if 'categoryId' in request.data:
            try:
                categoryId = request.data['categoryId']
                recipeCategory = RecipeCategory.objects.get(pk=categoryId)
                recipe.category = recipeCategory
            except RecipeImage.DoesNotExist:
                return JsonResponse({'isUpdated': False, 'errorMessage': "RecipeCategory does not exist"}, safe=False,
                                    status=status.HTTP_404_NOT_FOUND)
        if 'mainImageId' in request.data:
            try:
                mainImageId = request.data['mainImageId']
                recipeImage = RecipeImage.objects.get(pk=mainImageId)
                recipe.mainImage = recipeImage
            except RecipeImage.DoesNotExist:
                return JsonResponse({'isUpdated': False, 'errorMessage': "RecipeImage does not exist"}, safe=False,
                                    status=status.HTTP_404_NOT_FOUND)
            serializer = RecipeSerializer(recipe, data=request.data, partial=True)
            return create_response(serializer)


class RecipeDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecipeSerializer

    @swagger_auto_schema(tags=["recipe"])
    def delete(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return JsonResponse({'isDeleted': False, 'errorMessage': "Recipe does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        if recipe.author.id != request.user.id:
            return JsonResponse({'isDeleted': False, 'errorMessage': "User does not own the recipe"}, safe=False,
                                status=status.HTTP_401_UNAUTHORIZED)

        recipe.delete()
        return JsonResponse({'isDeleted': True}, safe=False,
                            status=status.HTTP_404_NOT_FOUND)


class RecipeCategoryView(GenericAPIView):
    serializer_class = RecipeCategorySerializer

    @swagger_auto_schema(tags=["recipe"])
    def get(self, request):
        categories = RecipeCategory.objects.all()
        serializer = RecipeCategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class RecipeCreateCommentView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer

    @swagger_auto_schema(tags=["recipe"],
                         request_body=Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 'recipeId': Schema(type=TYPE_INTEGER),
                                 'commentText': Schema(type=TYPE_STRING),
                                 'rating': Schema(type=TYPE_INTEGER)
                             }
                         ))
    def post(self, request):
        try:
            recipe = Recipe.objects.get(pk=request.data['recipeId'])
        except Recipe.DoesNotExist:
            return JsonResponse({'isDeleted': False, 'errorMessage': "Recipe does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['recipe'] = data['recipeId']
        data['author'] = request.user.id
        serializer = RatingSerializer(data=data)
        return create_response(serializer)
