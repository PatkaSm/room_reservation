from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    serializer.update(instance=request.user, validated_data=serializer.validated_data)
    return Response(data=serializer.data, status=status.HTTP_200_OK)