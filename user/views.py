from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


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
        print(serializer.data)
        data['fail'] = "Błąd rejestracji"
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

