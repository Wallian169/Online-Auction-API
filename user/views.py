from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from auction_api.models import Favorite, AuctionLot
from auction_api.serializers import AuctionLotSerializer
from user.models import User
from user.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserInfoSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

@extend_schema_view(
    get=extend_schema(
        summary="Get Favorite Lots",
        description="Returns a list of auction lots favorited "
                    "by the authenticated user.",
        responses={200: AuctionLotSerializer(many=True)},
    )
)
@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def get_favorites(request):
    """Return User favorite lots"""
    user = request.user
    favorites = Favorite.objects.filter(user=user).select_related("auction_lot").prefetch_related("auction_lot__images")

    lots = [fav.auction_lot for fav in favorites]
    serializer = AuctionLotSerializer(lots, many=True)

    return Response(serializer.data)


class UserAuctionLotListView(generics.ListAPIView):
    serializer_class = AuctionLotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AuctionLot.objects.filter(owner=self.request.user)

class UserContactsView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        return User.objects.filter(id=user_id)
