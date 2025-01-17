from django.utils.timezone import now
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

    def validate(self, data):
        errors = {}

        self.validate_initial_price(data, errors)
        self.validate_min_step(data, errors)
        self.validate_buyout_price(data, errors)
        self.validate_close_time(data, errors)

        if errors:
            raise serializers.ValidationError(errors)

        return data

    @staticmethod
    def validate_initial_price(data, errors):
        if data["initial_price"] <= 0:
            errors["initial_price"] = "Initial price must be greater than 0."

    @staticmethod
    def validate_min_step(data, errors):
        if data["min_step"] <= 0:
            errors["min_step"] = "Minimum step must be greater than 0."

    @staticmethod
    def validate_buyout_price(data, errors):
        if "initial_price" not in errors:
            if data["buyout_price"] <= data["initial_price"]:
                errors["buyout_price"] = "Buyout price must be greater than initial price."

    @staticmethod
    def validate_close_time(data, errors):
        if data["close_time"] <= now():
            errors["close_time"] = "Close time must be in the future."

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
            "is_active",
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

        if

        if value <= auction_lot.initial_price:
            raise serializers.ValidationError(
                "The bid must be higher then the initial price"
            )
        max_bid = auction_lot.bids.order_by("-offered_price").first()
        if max_bid and value <= max_bid.offered_price:
            raise serializers.ValidationError(
                "The bid must be higher then the current highest bid"
            )

        if max_bid and (value - max_bid.offered_price < auction_lot.min_step):
            raise serializers.ValidationError(
                "The difference between the new bid"
                " and the current highest bid must be "
                f"at least {auction_lot.min_step}."
            )

        return value
