from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from recipesBackend import views
from recipesBackend.views import CustomAuthToken, ProfileView


urlpatterns = [
    url(r'^api/register/$', views.userApi),
    url(r'^api/users/getUser/([0-9]+)$', views.userApi),
    url(r'^api/users/getAllUsers', views.allUsersApi),
    path('profile/', ProfileView.as_view()),
    path('api/auth/', CustomAuthToken.as_view()),
    url(r'^api/SaveFile$', views.SaveFile)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)