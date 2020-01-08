from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from django.core import serializers
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['success'] = 'Zarejestrowano pomyslnie'
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data['fail'] = "Błąd rejestracji"
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_details(request):
    data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'room_number': request.user.room_number,
        'phone_number': request.user.phone_number,
        'consultations': request.user.consultations
    }
    return Response(data=data, status=status.HTTP_200_OK)
