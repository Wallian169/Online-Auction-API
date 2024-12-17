from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import AuctionLot, Bid
from .serializers import AuctionLotSerializer, BidSerializer


class AuctionLotListCreateView(generics.ListCreateAPIView):
    queryset = AuctionLot.objects.all()
    serializer_class = AuctionLotSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class AuctionLotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuctionLot.objects.all()
    serializer_class = AuctionLotSerializer

class BidListCreateView(generics.ListCreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        auction_lot = AuctionLot.objects.get(pk=self.kwargs['pk'])
        return auction_lot.bids.all()

    def perform_create(self, serializer):
        auction_lot = AuctionLot.objects.get(pk=self.kwargs['pk'])
        serializer.save(bidder=self.request.user, auction_lot=auction_lot)