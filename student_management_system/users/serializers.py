from rest_framework import serializers
from .models import User
from students.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        ref_name = "CustomUserSerializer"


class UserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    ref_name = "CustomUserRegistrationSerializer"

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('re_password')

        user = User.objects.create_user(**validated_data, role=role)

        if role == 'student':
            Student.objects.create(user=user)

        return user
