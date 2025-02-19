from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from auction_api.models import Favorite
from auction_api.serializers import AuctionLotListSerializer
from user.serializers import UserSerializer, UserProfileSerializer


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
        responses={200: AuctionLotListSerializer(many=True)},
    )
)
@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def get_favorites(request):
    """Return User favorite lots"""
    user = request.user
    favorites = Favorite.objects.filter(user=user).select_related("auction_lot")

    lost = [fav.auction_lot for fav in favorites]
    serializer = AuctionLotListSerializer(lost, many=True)

    return Response(serializer.data)
