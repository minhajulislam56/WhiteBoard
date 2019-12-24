from accounts.models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'email_verified',
            'profile_pic',
            'bio',
            'signup_time',
            'login_time',
            'is_staff',
            'is_superuser'
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'bio',
        ]


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_pic']


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'profile_pic',
            'bio',
        ]