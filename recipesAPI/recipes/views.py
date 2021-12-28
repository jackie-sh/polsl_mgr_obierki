from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status


def get_recipe(request, id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)

def create_recipe(request):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)

def upload_main_image(request, id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)

def edit_recipe(request,id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)

def delete_recipe(request,id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)

def get_all(request):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)

def get_image(request, id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)

def create_comment(request, id):
    return JsonResponse({'temp': 'Mocked'}, status=status.HTTP_200_OK)