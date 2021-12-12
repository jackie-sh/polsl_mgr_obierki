from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
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


def username_exists(username):
    return User.objects.filter(username=username).exists()


@csrf_exempt
def allUsersApi(request):
    if request.method == 'GET':
        users = User.objects.values_list('id', 'name')
        user_serializer = UserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)


@csrf_exempt
def userApi(request, id=0):
    if request.method == 'GET':
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data['id'])
        return JsonResponse({'id': user['id'], 'name': user['name']}, safe=False)
    elif request.method == 'POST':
        users_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=users_data)
        if user_serializer.is_valid():
            if username_exists(users_data['name']):
                user_serializer.save()
                return JsonResponse({'isCreated': True, 'errorMessage': ""}, safe=False)
            return JsonResponse({'isCreated': True, 'errorMessage': "User already exists!"}, safe=False)
        return JsonResponse({'isCreated': False, 'errorMessage': "Incorrect json format!"}, safe=False)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user = User.objects.get(id=user_data['id'])
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'isUpdated': True, 'errorMessage': ""}, safe=False)
        return JsonResponse({'isUpdated': False, 'errorMessage': "Failed to update user!"}, safe=False)
    elif request.method == 'DELETE':
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse(f"User with id:{id} deleted!", safe=False)


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
