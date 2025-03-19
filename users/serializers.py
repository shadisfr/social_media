from rest_framework import serializers
from .models import CustomUser

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Ensure passwords match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """Remove password2 and create user"""
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user details (excluding passwords)"""

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "bio", "profile_picture"]


        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["followers"]



class FollowStatusSerializer(serializers.Serializer):
    message = serializers.CharField()
