from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from recipesBackend import views
from recipesBackend.views import CustomAuthToken, ProfileView

# url(r'^api/register/$', views.userApi),


urlpatterns = [
    url(r'^api/users/getAllUsers', views.getallUsersApi),
    url(r'^api/users/getUser/([0-9]+)$', views.getUserApi),
    url(r'^api/users/addUser/', views.addUserApi),
    url(r'^api/users/modifyUser/([0-9]+)$', views.modifyUserApi),
    url(r'^api/users/deleteUser/([0-9]+)$', views.deleteUserApi),
    path('profile/', ProfileView.as_view()),
    path('api/auth/', CustomAuthToken.as_view()),
    url(r'^api/SaveFile$', views.SaveFile)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)