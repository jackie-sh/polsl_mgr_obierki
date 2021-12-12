import json

from django.http import JsonResponse
from rest_framework import status
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.parsers import JSONParser, FileUploadParser
from django.views.decorators.csrf import csrf_exempt
from recipesBackend.models import User
from recipesBackend.serializers import UserSerializer, RecipeSerializer
from django.core.files.storage import default_storage
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


def username_exists_by_name(name):
    return User.objects.filter(name=name).exists()


def username_exists_by_id(id):
    return User.objects.filter(id=id).exists()


@csrf_exempt
def getallUsersApi(request):
    if request.method == 'GET':
        users = User.objects.values_list('id', 'name')
        user_serializer_raw = json.dumps(list(users), cls=DjangoJSONEncoder)
        return JsonResponse(user_serializer_raw, safe=False)


@csrf_exempt
def getUserApi(request, id=0):
    if request.method == 'GET':
        if username_exists_by_id(id):
            user = User.objects.get(id=id)
            return JsonResponse({'id': user.id, 'name': user.name}, safe=False)
        return JsonResponse({'errorMessage': "User with given id does not exist!"}, safe=False)
    return JsonResponse({'errorMessage': "This endpoint only serves gets!"}, safe=False)



@csrf_exempt
def addUserApi(request, id=0):
    if request.method == 'POST':
        users_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=users_data)
        if user_serializer.is_valid():
            if not username_exists_by_name(user_serializer.validated_data['name']):
                user_serializer.save()
                return JsonResponse({'isCreated': True, 'errorMessage': ""}, safe=False)
            return JsonResponse({'isCreated': False, 'errorMessage': "User already exists!"}, safe=False)
        return JsonResponse({'isCreated': False, 'errorMessage': "Incorrect json format!"}, safe=False)
    return JsonResponse({'isCreated': False, 'errorMessage': "This endpoint only serves posts!"}, safe=False)


@csrf_exempt
def modifyUserApi(request, id=0):
    if request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data.id)
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


@csrf_exempt
def SaveFile(request):
    file = request.FILES['uploadedFile']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)


class ProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.name,
            'user_id': user.pk,
            'email': user.email
        })


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = RecipeSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
