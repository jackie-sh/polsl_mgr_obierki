from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from recipesBackend import views
from recipesBackend.views import CustomAuthToken, ProfileView


urlpatterns = [
    url(r'^api/users/getAllUsers', views.getallUsersApi),
    url(r'^api/users/getUser/([0-9]+)$', views.getUserApi),
    url(r'^api/users/addUser/', views.addUserApi),
    url(r'^api/users/modifyUser/([0-9]+)$', views.modifyUserApi),
    url(r'^api/users/deleteUser/([0-9]+)$', views.deleteUserApi),
    path('profile/', ProfileView.as_view()),
<<<<<<< HEAD
    path('api/register', CustomAuthToken.as_view()),
=======
    path('api/register/', CustomAuthToken.as_view()),
>>>>>>> 5c18b700c7e118ab89c4831cbe9cf7a8e36940cf
    url(r'^api/recipes/upload-main-image', views.SaveFile)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)