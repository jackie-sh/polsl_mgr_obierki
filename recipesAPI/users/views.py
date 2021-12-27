from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from django.shortcuts import render
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from users.models import User
from users.serializers import UserSerializer, LoginSerializer

from django.conf import settings
from django.contrib import auth
import jwt


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'isCreated': True}
            return JsonResponse(data, status=status.HTTP_201_CREATED)

        data = {'isCreated': True, 'errorMessage': serializer.errors}
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")

            serializer = UserSerializer(user)

            data = {'id': user.id ,'token': auth_token}

            return JsonResponse(data, status=status.HTTP_200_OK)

            # SEND RES
        return JsonResponse({'errorMessage': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
def getallUsersApi(request):
    if request.method == 'GET':
        users = User.objects.values_list('id', 'username')
        user_serializer_raw = json.dumps(list(users), cls=DjangoJSONEncoder)
        return JsonResponse(user_serializer_raw, safe=False)


@csrf_exempt
def getUserApi(request, id=0):
    if request.method == 'GET':
        if username_exists_by_id(id):
            user = User.objects.get(id=id)
            return JsonResponse({'id': user.id, 'username': user.username}, safe=False)
        return JsonResponse({'errorMessage': "User with given id does not exist!"}, safe=False)
    return JsonResponse({'errorMessage': "This endpoint only serves gets!"}, safe=False)



@csrf_exempt
def addUserApi(request, id=0):
    if request.method == 'POST':
        users_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=users_data)
        try:
            if user_serializer.is_valid(raise_exception=True):
                if not username_exists_by_name(user_serializer.validated_data['username']):
                    user_serializer.save()
                    return JsonResponse({'isCreated': True, 'errorMessage': ""}, safe=False)
                return JsonResponse({'isCreated': False, 'errorMessage': "User already exists!"}, safe=False)
            return JsonResponse({'isCreated': False, 'errorMessage': "Incorrect json format!"}, safe=False)
        except serializers.ValidationError as valEr:
            return JsonResponse({'isCreated': False, 'errorMessage': valEr.detail}, safe=False)
    return JsonResponse({'isCreated': False, 'errorMessage': "This endpoint only serves posts!"}, safe=False)


@csrf_exempt
def modifyUserApi(request, id=0):
    if request.method == 'PUT':
        user_data = JSONParser().parse(request)
        if not username_exists_by_id(id):
            return JsonResponse({'isUpdated': False, 'errorMessage': "User with given id does not exist!"}, safe=False)
        user = User.objects.get(id=id)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'isUpdated': True, 'errorMessage': ""}, safe=False)
        return JsonResponse({'isUpdated': False, 'errorMessage': "Failed to update user!"}, safe=False)
    return JsonResponse({'isUpdated': False, 'errorMessage': "This endpoint only serves puts!"}, safe=False)


@csrf_exempt
def deleteUserApi(request, id=0):
    if request.method == 'DELETE':
        if username_exists_by_id(id):
            User.objects.get(id=id).delete()
            return JsonResponse({'isDeleted': True, 'errorMessage': ""}, safe=False)
        return JsonResponse({'isDeleted': False, 'errorMessage': " User with given id does not exist!"}, safe=False)
    return JsonResponse({'isDeleted': False, 'errorMessage': "This endpoint only serves deletes!"}, safe=False)




def username_exists_by_name(name):
    return User.objects.filter(username=name).exists()


def username_exists_by_id(id):
    return User.objects.filter(id=id).exists()
