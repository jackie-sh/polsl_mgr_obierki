from django.urls import path

from recipesAPI.recipes import views

urlpatterns = [
      path('api/recipes/get-recipe/<int:pk>', views.RecipeDetails.as_view()),
      path('api/recipes/delete-recipe/<int:pk>', views.RecipeDetails.as_view()),
      path('api/recipes/create-recipe/',        views.RecipeInit.as_view()),
      path('api/recipes/modify-recipe/<int:pk>', views.RecipeDetails.as_view()),

]