from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path('reservation/<pk>/detail/', views.reservation_detail, name='reservation_detail'),
    path('reservation/<pk>/delete/', views.reservation_delete, name='reservation_delete'),
    path('create/', views.reservation_create, name='add_reservation'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('all_reservations/', views.all_reservations, name='all_reservations'),

]