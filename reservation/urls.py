from django.urls import path, include
from .import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('reservation', views.ReservationView,  base_name='register')


urlpatterns = [
    path('', include(router.urls)),
    path('reservation/<pk>/detail', views.reservation_detail),
    path('reservation/<pk>/delete', views.reservation_delete),
    path('create', views.reservation_create),
]