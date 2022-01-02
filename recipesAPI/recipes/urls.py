from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from recipes import views

urlpatterns = [
    path('get-recipe/<int:pk>', views.RecipeGetView.as_view(http_method_names=['get'])),
    path('create-recipe', views.RecipeCreateView.as_view(http_method_names=['post'])),
    path('upload-main-image/<int:pk>', views.RecipeUploadImage.as_view(http_method_names=['post'])),
    path('edit-recipe/<int:pk>',  views.RecipeEditView.as_view(http_method_names=['put'])),
    path('delete-recipe/<int:pk>', views.RecipeDeleteView.as_view()),
    path('get-all', views.get_all),
    path('get-image/<int:id>', views.RecipeGetImage.as_view(http_method_names=['get'])),
    path('create-comment', views.RecipeCreateCommentView.as_view()),
    path('get-categories', views.RecipeCategoryView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
