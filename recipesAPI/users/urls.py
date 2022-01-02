from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views
from users.views import *

urlpatterns = [
    path('api/users/getAllUsers', views.UserList.as_view()),
    path('api/users/addUser/', views.UserList.as_view()),
    path('api/users/getUser/<int:pk>', views.UserDetail.as_view()),
    path('api/users/modifyUser/<int:pk>', views.UserDetail.as_view()),
    path('api/users/deleteUser/<int:pk>', views.UserDetail.as_view()),
    path('api/register', RegisterView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/refresh-token', LoginRefreshView.as_view(http_method_names=['post'])),
]