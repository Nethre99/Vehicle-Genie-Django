from app import views
from django.urls import path

urlpatterns = [
    path('index/', views.index),
    path('getAll/', views.getAllVehicles),
    path('getById/<int:pk>/', views.getById),
    path('addVehicle/', views.addVehicle),
    path('getUserVehicle/', views.getUserVehicles),
    path('getRecommendations/<int:UserId>/', views.getRecommendations),
]
