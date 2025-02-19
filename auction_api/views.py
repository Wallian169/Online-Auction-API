from django.db.models import Count
from django.db.models.functions import Random
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auction_api.models import AuctionLot, Bid, Category
from auction_api.serializers import (
    AuctionLotBaseSerializer,
    AuctionLotSerializer,
    BidSerializer,
    AuctionLotDetailSerializer,
    CategorySerializer,
    AuctionLotListSerializer,
)


class AuctionLotViewSet(viewsets.ModelViewSet):
    queryset = AuctionLot.objects.all()
    serializer_class = AuctionLotSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return AuctionLotBaseSerializer
        if self.action == "detail":
            return AuctionLotDetailSerializer
        if self.action == "list":
            return AuctionLotListSerializer
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
        "top_lots": AuctionLotListSerializer(top_lots, many=True).data,
        "new": AuctionLotListSerializer(new, many=True).data,
        "also_like": AuctionLotListSerializer(also_like, many=True).data,
    }

    return Response(response_data)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
