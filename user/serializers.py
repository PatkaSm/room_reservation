from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'is_active', 'phone_number', 'room_number',
                  'consultations']

    def create(self, validates_data):
        return User.objects.create_user(**validates_data)

    def createStaffUser(self, validates_data):
        return User.objects.create_staffuser(**validates_data)

    def createAdminUser(self, validates_data):
        return User.objects.create_superuser(**validates_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.room_number = validated_data.get('room_number', instance.room_number)
        instance.consultations = validated_data.get('consultations', instance.consultations)
        if validated_data.get('password'):
            instance.set_password(raw_password=validated_data.get('password'))
        instance.save()
        return instance
