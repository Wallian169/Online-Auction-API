from rest_framework import serializers
from auction_api.models import AuctionLot, Bid


class AuctionLotBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionLot
        fields = [
            "item_name",
            "description",
            "location",
            "category_id",
            "initial_price",
            "min_step",
            "buyout_price",
            "close_time",
        ]

class AuctionLotSerializer(AuctionLotBaseSerializer):

    class Meta:
        model = AuctionLot
        fields = [
            "id",
            "item_name",
            "description",
            "location",
            "category_id",
            "initial_price",
            "min_step",
            "buyout_price",
            "close_time",
            "owner_id",
            "winner_id",
        ]

class AuctionLotDetailSerializer(serializers.ModelSerializer):
    bids = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AuctionLot
        fields = [
            "id",
            "item_name",
            "description",
            "location",
            "category_id",
            "initial_price",
            "min_step",
            "buyout_price",
            "close_time",
            "owner_id",
            "bids",
            "winner_id",
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
            raise serializers.ValidationError("AuctionLot was not found")

        if value <= auction_lot.initial_price:
            raise serializers.ValidationError(
                "The bid must be higher then the initial price"
            )
        max_bid = auction_lot.bids.order_by("-offered_price").first()
        if max_bid and value <= max_bid.offered_price:
            raise serializers.ValidationError(
                "The bid must be higher then the current highest bid"
            )

        if max_bid and ((max_bid.offered_price - value) < auction_lot.min_step):
            raise serializers.ValidationError(
                "The difference between the new bid"
                " and the current highest bid must be "
                f"at least {auction_lot.min_step}."
            )

        return value
