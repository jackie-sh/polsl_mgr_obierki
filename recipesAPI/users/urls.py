from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from users import views
from users.views import RegisterView, LoginView

urlpatterns = [
      url(r'^api/users/getAllUsers', views.getallUsersApi),
      url(r'^api/users/getUser/([0-9]+)$', views.getUserApi),
      url(r'^api/users/addUser/', views.addUserApi),
      url(r'^api/users/modifyUser/([0-9]+)$', views.modifyUserApi),
      url(r'^api/users/deleteUser/([0-9]+)$', views.deleteUserApi),
      path('api/register', RegisterView.as_view()),
      path('api/login', LoginView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)