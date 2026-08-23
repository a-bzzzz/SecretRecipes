from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search, name='search'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='rbook/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
