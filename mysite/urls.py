"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from user.views import user_register, user_details, update_profile, is_admin, get_users, delete_user, set_admin, \
    set_active, AuthToken
from log.views import LogsPDFView
from reservation_season.views import get_season, new_season

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', include('room.urls')),
    path('reservations/', include('reservation.urls')),
    url(r'^login/', AuthToken.as_view()),
    path('users/register/', user_register, name='register'),
    path('user/details/', user_details, name='details'),
    path('user/update_profile/', update_profile, name='update_profile'),
    path('logs/get/', LogsPDFView.as_view(), name='get_logs'),
    path('users/is_admin/', is_admin, name='is_admin'),
    path('users/get_users/', get_users, name='get_users'),
    path('seasons/get_season/', get_season, name='get_season'),
    path('season/new/', new_season, name='new_season'),
    path('users/<pk>/delete/', delete_user, name='delete_user'),
    path('users/set_admin/', set_admin, name='set_admin'),
    path('users/set_active/', set_active, name='set_active'),
]
