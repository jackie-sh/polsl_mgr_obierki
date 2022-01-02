import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse, Http404
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe, RecipeCategory
from .serializers import RecipeSerializer, RecipeCategorySerializer
from .models import Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
from rest_framework import status

def upload_main_image(request, id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)


def get_all(request):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)


def get_image(request, id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)


def create_comment(request, id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)


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
                    'categoryId': Schema(type=TYPE_INTEGER),
                    'shortDescription': Schema(type=TYPE_STRING),
                    'mainImageId': Schema(type=TYPE_INTEGER)
                })
         }
     )
    def get(self, request, pk, format=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Http404:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        recipe_serializer = RecipeSerializer(recipe, data={'view_count': recipe.view_count + 1}, partial=True)
        try:
            if recipe_serializer.is_valid(raise_exception=True):
                recipe_serializer.save()
                return JsonResponse(recipe_serializer.data, safe=False, status=status.HTTP_200_OK)
        except serializers.ValidationError as valEr:
            return JsonResponse({'errorMessage': valEr.detail}, status=status.HTTP_400_BAD_REQUEST)

class RecipeCreateView(GenericAPIView):
    serializer_class = RecipeSerializer

    @swagger_auto_schema(tags=["recipe"],
         request_body= Schema(
            type=TYPE_OBJECT,
            properties={
                'title': Schema(type=TYPE_STRING),
                'content': Schema (type=TYPE_STRING),
                'categoryId': Schema (type=TYPE_INTEGER),
                'shortDescription': Schema(type=TYPE_STRING),
                'mainImageId' : Schema(type=TYPE_INTEGER)
            }
        ),
        responses = {
            status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                properties={'isCreated': Schema(type=TYPE_BOOLEAN)}
            )
        }
    )
    def post(self, request):
        data = request.data
        data['category'] = data['categoryId']
        data['author'] = request.user.id
        data['view_count'] = 0
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'isCreated': True}
            return JsonResponse(data, status=status.HTTP_201_CREATED)

        data = {'isCreated': False, 'errorMessage': serializer.errors}
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class RecipeEditView(GenericAPIView):
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
    def put(self, request, pk, format=None):
        try:
            recipe = recipe = Recipe.objects.get(pk=pk)
        except Http404:
            return JsonResponse({'isUpdated': False, 'errorMessage': "Recipe does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        recipe_serializer = RecipeSerializer(recipe, data=request.data, partial=True)
        try:
            if recipe_serializer.is_valid(raise_exception=True):
                recipe_serializer.save()
                return JsonResponse({'isUpdated': True, 'errorMessage': ""}, status=status.HTTP_200_OK)
        except serializers.ValidationError as valEr:
            return JsonResponse({'isUpdated': False, 'errorMessage': valEr.detail}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)


class RecipeDeleteView(GenericAPIView):
    serializer_class = RecipeSerializer

    @swagger_auto_schema(tags=["recipe"])
    def delete(self, request, pk, format=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Http404:
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
    def get(self,request):
        categories = RecipeCategory.objects.all()
        serializer = RecipeCategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
