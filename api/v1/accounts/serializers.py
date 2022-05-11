from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super(UserTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(cls, attrs):
        data = super(UserTokenObtainPairSerializer, cls).validate(attrs)
        refresh = cls.get_token(cls.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "fullname",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "photo",
            "is_librarian",
            "customer_id",
        )
