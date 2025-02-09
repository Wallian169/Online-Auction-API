from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auction_api.models import AuctionLot, Bid, Category
from auction_api.serializers import (
    AuctionLotBaseSerializer,
    AuctionLotSerializer,
    BidSerializer,
    AuctionLotDetailSerializer,
)

@extend_schema_view(
    toggle_favourite=extend_schema(
        summary="Toggle favourite status of an auction lot",
        description="Adds or removes an auction lot from the user's favourites.",
        parameters=[OpenApiParameter(name="pk", description="Auction Lot ID", required=True, type=int)],
        responses={200: {"message": "Auction lot removed from favourites."}, 201: {"message": "Auction lot added to favourites."}},
    ),
    favourites=extend_schema(
        summary="Get all favourite auction lots",
        description="Returns a list of auction lots that the user has marked as favourites.",
        responses={200: AuctionLotSerializer(many=True)},
    ),
)
class AuctionLotViewSet(viewsets.ModelViewSet):
    queryset = AuctionLot.objects.all()
    serializer_class = AuctionLotSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post", "get"])
    @extend_schema(
        summary="Toggle favourite status",
        description="Adds the auction lot to favourites if not already present; removes it if it is.",
        parameters=[OpenApiParameter(name="pk", description="Auction Lot ID", required=True, type=int)],
        responses={
            200: {"message": "Auction lot removed from favourites."},
            201: {"message": "Auction lot added to favourites."},
        },
    )
    def toggle_favourite(self, request, pk=None):
        auction_lot = self.get_object()
        user = request.user

        if request.method == "GET":
            is_favourited = user in auction_lot.favourites.all()
            return Response(
                {"is_favourited": is_favourited},
                status=status.HTTP_200_OK,
            )

        if user in auction_lot.favourites.all():
            auction_lot.favourites.remove(user)
            return Response(
                {"message": "Auction lot removed from favourites."},
                status=status.HTTP_200_OK,
            )
        else:
            auction_lot.favourites.add(user)
            return Response(
                {"message": "Auction lot added to favourites."},
                status=status.HTTP_201_CREATED,
            )

    @action(detail=False, methods=["get"])
    @action(detail=False, methods=["get"])
    @extend_schema(
        summary="List favourite auction lots",
        description="Returns a list of auction lots that the user has marked as favourites.",
        responses={200: AuctionLotSerializer(many=True)},
    )
    def favourites(self, request):
        user = request.user
        favourite_lots = AuctionLot.objects.filter(favourites=user)
        serializer = AuctionLotSerializer(favourite_lots, many=True, context={"request": request})
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return AuctionLotBaseSerializer
        if self.action == "detail":
            return AuctionLotDetailSerializer
        if self.action == "place-bid":
            return BidSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class BidListCreateView(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auction_lot = AuctionLot.objects.get(pk=self.kwargs["pk"])
        return auction_lot.bids.all()

    def perform_create(self, serializer):
        auction_lot = AuctionLot.objects.get(pk=self.kwargs["pk"])
        serializer.save(bidder=self.request.user, auction_lot=auction_lot)

# def main_page(request):
#     top_categories = Category.objects.all()[:3]
#     lots = AuctionLot.objects.all().select_related("bids")
#
#     newest_lots = lots.order_by("-created_at")[:4]
#     most_popular = lots.annotate(bid_count=Count("bids")).order_by("-bid_count")[:4]
#
#     responce_data = {
#         "top_categories": Categories,
#     }