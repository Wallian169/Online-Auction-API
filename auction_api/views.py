from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AuctionLot
from .serializers import AuctionLotSerializer, BidSerializer


class AuctionLotListCreateView(generics.ListCreateAPIView):
    queryset = AuctionLot.objects.all()
    serializer_class = AuctionLotSerializer


class AuctionLotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuctionLot.objects.all()
    serializer_class = AuctionLotSerializer

class BidListCreateView(APIView):
    def get(self, request, pk):
        auction_lot = AuctionLot.objects.get(pk=pk)
        bids = auction_lot.bids.all()
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        auction_lot = AuctionLot.objects.get(pk=pk)
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(bidder=request.user, auction_lot=auction_lot)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)