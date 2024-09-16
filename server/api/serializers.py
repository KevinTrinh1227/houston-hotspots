from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]  # Include email, first_name, last_name
        extra_kwargs = {
            "password": {"write_only": True},  # Ensure the password isn't returned in API responses
        }

    def create(self, validated_data):
        # Extract the fields we want to handle manually
        email = validated_data['email']
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        password = validated_data['password']

        # Create the user without a username (email as username)
        user = User.objects.create_user(
            username=email,  # Use email as the username since Django requires this field
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password  # Password will be hashed automatically
        )
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {
            "author": {"read_only": True}  # Make author read-only as it will be automatically set
        }
