import rest_framework_simplejwt.views
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse, Http404
from drf_yasg.openapi import Schema, TYPE_STRING, TYPE_OBJECT
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from django.shortcuts import render
import json
import django.core

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import UserSerializer, LoginSerializer
from django.contrib import auth


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["user"])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'isCreated': True}
            return JsonResponse(data, status=status.HTTP_201_CREATED)

        data = {'isCreated': False, 'errorMessage': serializer.errors}
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["user"],
         request_body= Schema(
            type=TYPE_OBJECT,
            properties={
                'username': Schema(type=TYPE_STRING),
                'password': Schema (type=TYPE_STRING),
            }
        )
    )
    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            token = RefreshToken.for_user(user)
            data = {'id': user.id, 'accessToken': str(token.access_token), 'refreshToken': str(token)}
            return JsonResponse(data, status=status.HTTP_200_OK)

        return JsonResponse({'errorMessage': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginRefreshView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=["user"],
                         request_body=Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 'refreshToken': Schema(type=TYPE_STRING)
                             }
                         )
                     )
    def post(self, request):
        token = RefreshToken(request.data['refreshToken'])
        return JsonResponse({'accessToken': str(token.access_token)}, status=status.HTTP_501_NOT_IMPLEMENTED)

class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
        except Http404:
            return JsonResponse({'isDeleted': False, 'errorMessage': "User does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'id': user.id, 'username': user.username}, safe=False, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
        except Http404:
            return JsonResponse({'isUpdated': False, 'errorMessage': "User does not exists"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        user_serializer = UserSerializer(user, data=request.data)
        try:
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return JsonResponse({'isUpdated': True, 'errorMessage': ""}, safe=False, status=status.HTTP_200_OK)
        except serializers.ValidationError as valEr:
            return JsonResponse({'isUpdated': False, 'errorMessage': valEr.detail}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = self.get_object(pk)
        except Http404:
            return JsonResponse({'isDeleted': False, 'errorMessage': "User does not exist"}, safe=False,
                                status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return JsonResponse({'isDeleted': True, 'errorMessage': ""}, safe=False,
                            status=status.HTTP_204_NO_CONTENT)


    def user_exists_by_name(self, name):
        return User.objects.filter(username=name).exists()

    def get(self, request, format=None):
        users = User.objects.values('id', 'username')
        data = json.dumps(list(users), cls=DjangoJSONEncoder)
        return HttpResponse(data, content_type="application/json")

    def post(self, request, pk, format=None):
        user_serializer = UserSerializer(data=request.data)
        try:
            if user_serializer.is_valid(raise_exception=True):
                if not self.user_exists_by_name(user_serializer.validated_data['username']):
                    user_serializer.save()
                    return JsonResponse({'isCreated': True, 'errorMessage': ""}, safe=False,
                                        status=status.HTTP_201_CREATED)
                return JsonResponse({'isCreated': False, 'errorMessage': user_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as valEr:
            return JsonResponse({'isCreated': False, 'errorMessage': valEr.detail}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)


