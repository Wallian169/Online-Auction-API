from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer, UserProfileSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
