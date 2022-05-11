from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User

from .serializers import UserTokenObtainPairSerializer,UserSerializer
from six import text_type

class MyObtainTokenPairView(TokenObtainPairView):
    """
    View to generate access and refresh token with username and password
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = text_type(refresh)
        data["access"] = text_type(refresh.access_token)

        return data


class MyProfileView(APIView):
    """
    View to get all information associated with current user
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserProfileView(RetrieveAPIView):
    """
    View to get all information associated with user identified by pk
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
