from django.http import JsonResponse, HttpResponse, Http404
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe
from .serializers import RecipeSerializer
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


class RecipeDetails(APIView):

    def get_message_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get_recipe_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    #@swagger_auto_schema(tags=["recipe"])
    def get(self, request, pk, format=None):
        try:
            recipe = self.get_recipe_object(pk)
        except Http404:
            return JsonResponse({'isUpdated': False, 'errorMessage': "Recipe does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        recipe_serializer = RecipeSerializer(recipe, data=request.data)
        try:
            if recipe_serializer.is_valid(raise_exception=True):
                recipe_serializer['views'] += 1
                recipe_serializer.save()
                recipe_modified = self.get_recipe_object(pk)
                recipe_serializer_modified = RecipeSerializer(recipe, data=request.data)
                messsage = self.get_message_object(pk)
                # TODO: Get list of messages and attach to recipe, calculate mean of recipe from comments
                return JsonResponse(recipe_serializer_modified.data, safe=False, status=status.HTTP_200_OK)
        except serializers.ValidationError as valEr:
            return JsonResponse({'isUpdated': False, 'errorMessage': valEr.detail}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)

    #@swagger_auto_schema(tags=["recipe"])
    def put(self, request, pk, format=None):
        try:
            recipe = self.get_recipe_object(pk)
        except Http404:
            return JsonResponse({'isUpdated': False, 'errorMessage': "Recipe does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        recipe_serializer = RecipeSerializer(recipe, data=request.data)
        try:
            if recipe_serializer.is_valid(raise_exception=True):
                recipe_serializer.save()
                return JsonResponse({'isUpdated': True, 'errorMessage': ""}, safe=False, status=status.HTTP_200_OK)
        except serializers.ValidationError as valEr:
            return JsonResponse({'isUpdated': False, 'errorMessage': valEr.detail}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)

    #@swagger_auto_schema(tags=["recipe"])
    def delete(self, request, pk, format=None):
        try:
            user = self.get_recipe_object(pk)
        except Http404:
            return JsonResponse({'isUpdated': False, 'errorMessage': "Recipe does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeView(GenericAPIView):
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

