from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auction_api.models import (
    AuctionLot,
    Bid,
    Category,
    Favorite,
    AuctionLotFilter
)
from auction_api.serializers import (
    AuctionLotSerializer,
    BidSerializer,
    CategorySerializer,
    AuctionLotCreateSerializer,
    AuctionLotListDetailSerializer,
)


class AuctionLotViewSet(viewsets.ModelViewSet):
    queryset = AuctionLot.objects.prefetch_related('bids__bidder').all()
    serializer_class = AuctionLotListDetailSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = AuctionLotFilter

    @extend_schema(
        summary="Toggle Favorite Lot",
        description="Add or remove an auction lot from the user's favorites.",
        responses={
            200: {
                "description": "Success message",
                "content": {
                    "application/json": {
                        "example": {"detail": "Lot added to favorites."}
                    }
                },
            },
            404: {
                "description": "Lot not found",
                "content": {
                    "application/json": {
                        "example": {"detail": "Lot not found."}
                    }
                },
            },
        },
        request=None,
    )
    @action(detail=True, methods=["POST"])
    def toggle_favorite(self, request, pk=None):
        """
        Toggle a lot in the user's favorites.
        Adds or removes the lot from the user's favorites.
        """
        user = request.user
        lot = get_object_or_404(AuctionLot, pk=pk)
        favorite, created = Favorite.objects.get_or_create(user=user, auction_lot=lot)

        if created:
            message = "Lot added to favorites."
        else:
            favorite.delete()
            message = "Lot removed from favorites."

        return Response({"detail": message}, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="categories",
                description="Filter by multiple category IDs",
                required=False,
                type={"type": "array", "items": {"type": "integer"}},
                style="form",
                explode=True,
            ),
            OpenApiParameter(name="name", description="Filter by fragment of name", required=False, type=str),
            OpenApiParameter(
                name="price_max",
                description="Filter max price",
                required=False,
                type={"type": "number", "format": "decimal"}
            ),
            OpenApiParameter(
                name="price_min",
                description="Filter by minimum price",
                required=False,
                type={"type": "number", "format": "decimal"}
            ),
            OpenApiParameter(
                name="created_after",
                description="Filter lots created after this datetime (ISO 8601 format, ect. 2025-05-03T14:30:00Z)",
                required=False,
                type={"type": "string", "format": "date-time"}
            ),
            OpenApiParameter(
                name="created_before",
                description="Filter lots created before this datetime (ISO 8601 format, ect. 2025-05-03T14:30:00Z)",
                required=False,
                type={"type": "string", "format": "date-time"}
            ),
            OpenApiParameter(
                name="close_after",
                description="Filter lots closing after this datetime (ISO 8601 format, ect. 2025-05-03T14:30:00Z)",
                required=False,
                type={"type": "string", "format": "date-time"}
            ),
            OpenApiParameter(
                name="close_before",
                description="Filter lots closing before this datetime (ISO 8601 format, ect. 2025-05-03T14:30:00Z)",
                required=False,
                type={"type": "string", "format": "date-time"}
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """This is the list view."""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return AuctionLotCreateSerializer
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
        auction_lot.last_price = serializer.validated_data["offered_price"]
        auction_lot.save()
        serializer.save(bidder=self.request.user, auction_lot=auction_lot)


@api_view(["GET"])
def main_page(request):
    """Main page of the API"""
    top_categories = Category.objects.all()[:3]
    all_lots = AuctionLot.objects.all()

    top_lots = all_lots.annotate(bids_sum=Count("bids")).order_by("-bids_sum")[:3]
    new = all_lots.order_by("-created_at")[:4]
    also_like = all_lots.order_by("?")[:12]

    response_data = {
        "categories": CategorySerializer(top_categories, many=True).data,
        "top_lots": AuctionLotSerializer(top_lots, many=True).data,
        "new": AuctionLotSerializer(new, many=True).data,
        "also_like": AuctionLotSerializer(also_like, many=True).data,
    }

    return Response(response_data)

class CategoryListView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
