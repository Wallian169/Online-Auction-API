from rest_framework import serializers
from auction_api.models import AuctionLot, Bid

class AuctionLotSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    bids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    images = serializers.ImageField(use_url=True)

    class Meta:
        model = AuctionLot
        fields = ["id", "item_name", "description", "created_at", "initial_price", "close_time", "images", "owner", "bids"]


class BidSerializer(serializers.Serializer):
    bidder = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "auction_lot", "offered_price", "bidder", "bid_time"]