from django.urls import path

from recipes import views

urlpatterns = [
    path('get-recipe/<int:pk>/', views.RecipeGetView.as_view(http_method_names=['get'])),
    path('create-recipe/', views.RecipeCreateView.as_view(http_method_names=['post'])),
    path('upload-main-image/<int:pk>/', views.upload_main_image),
    path('edit-recipe/<int:pk>/',  views.RecipeDetails.as_view()),
    path('delete-recipe/<int:pk>/', views.RecipeDetails.as_view()),
    path('get-all/', views.get_all),
    path('get-image/<int:id>/', views.get_image),
    path('create-comment/<int:id>/', views.create_comment),
]