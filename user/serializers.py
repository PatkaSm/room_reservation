from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'password', 'first_name', 'last_name', 'is_active']

    def create(self, validates_data):
        return User.objects.create_user(**validates_data)

    def createStaffUser(self, validates_data):
        return User.objects.create_staffuser(**validates_data)

    def createAdminUser(self, validates_data):
        return User.objects.create_superuser(**validates_data)
