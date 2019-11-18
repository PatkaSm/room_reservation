from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('room', views.RoomView)

urlpatterns = [
    path('', include(router.urls)),
    path('show_available_rooms', views.show_available_rooms)
]
