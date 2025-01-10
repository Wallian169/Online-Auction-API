from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from auction_api.models import AuctionLot, Bid
from auction_api.serializers import (
    AuctionLotBaseSerializer,
    AuctionLotSerializer,
    BidSerializer,
    AuctionLotDetailSerializer,
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
