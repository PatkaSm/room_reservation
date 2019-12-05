from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('show_available_rooms/', views.show_available_rooms, name='show_available_rooms')
]
