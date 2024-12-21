from rest_framework import serializers
from auction_api.models import AuctionLot, Bid

class AuctionLotSerializer(serializers.ModelSerializer):
    bids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    images = serializers.ImageField(use_url=True)

    class Meta:
        model = AuctionLot
        fields = [
            "id",
            "item_name",
            "description",
            "created_at",
            "initial_price",
            "close_time",
            "images",
            "bids"
        ]

class BidSerializer(serializers.ModelSerializer):
    bidder = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "auction_lot", "offered_price", "bidder", "bid_time"]

    def validate_offered_price(self, value):
        auction_lot = self.initial_data.get("auction_lot")
        try:
            auction_lot = AuctionLot.objects.get(pk=auction_lot)
        except AuctionLot.DoesNotExist:
            raise serializers.ValidationError("Auction Lot wasn`t found")

        if value <= auction_lot.initial_price:
            raise serializers.ValidationError(
                "The bid must be higher then the initial price"
            )
        max_bid = auction_lot.bids.order_by("-offered_price").first()
        if max_bid and value <= max_bid.offered_price:
            raise serializers.ValidationError(
                "The bid must be higher then the current highest bid"
            )

        return value