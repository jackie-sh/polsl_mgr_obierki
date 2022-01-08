from django.http import JsonResponse, HttpResponse
from drf_yasg.openapi import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView

from chat.serializers import *
from recipes.views import create_response
from users.models import User


class ViewMessagesView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializerGet

    @swagger_auto_schema(tags=["messages"],
                         manual_parameters=[
                             Parameter('toUserId', IN_QUERY, type='integer'),
                         ])
    def get(self, request):
        target_id = int(request.GET['toUserId'])
        messages = request.user.messages_sent.filter(to_user=target_id)
        messages_serializer = MessageSerializerGet(messages, many=True)
        return JsonResponse(messages_serializer.data, safe=False, status=status.HTTP_200_OK)


class SendMessageView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializerCreate

    @swagger_auto_schema(tags=["messages"],
                         request_body=Schema(
                             type=TYPE_OBJECT,
                             properties={
                                 'toUserId': Schema(type=TYPE_INTEGER),
                                 'message': Schema(type=TYPE_STRING)
                             }
                         ),
                         responses={
                             status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                                        properties={'isCreated': Schema(type=TYPE_BOOLEAN),
                                                                    'id': Schema(type=TYPE_INTEGER)}
                                                        )
                         })
    def post(self, request):
        data = request.data
        data['from_user'] = request.user.id
        data['to_user'] = data['toUserId']
        new_message = MessageSerializerCreate(data=data)
        return create_response(new_message)
