from django.conf.urls import url
from recipesBackend import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^user/$', views.userApi),
    url(r'^user/([0-9]+)$', views.userApi),
    url(r'^SaveFile$', views.SaveFile)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
