from django.db.models import Max
from django.utils import timezone
from rest_framework import serializers

from auction_api.models import AuctionLot, Bid, Category


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

        self._validate_initial_price(data, errors)
        self._validate_min_step(data, errors)
        self._validate_buyout_price(data, errors)
        self._validate_close_time(data, errors)

        if errors:
            raise serializers.ValidationError(errors)

        return data

    @staticmethod
    def _validate_initial_price(data, errors):
        if data["initial_price"] <= 0:
            errors["initial_price"] = "Initial price must be greater than 0."

    @staticmethod
    def _validate_min_step(data, errors):
        if data["min_step"] <= 0:
            errors["min_step"] = "Minimum step must be greater than 0."

    @staticmethod
    def _validate_buyout_price(data, errors):
        if "initial_price" not in errors:
            if data["buyout_price"] <= data["initial_price"]:
                errors["buyout_price"] = "Buyout price must be greater than initial price."

    @staticmethod
    def _validate_close_time(data, errors):
        print(data["close_time"])
        if data["close_time"] <= timezone.now():
            errors["close_time"] = "Close time must be in the future."

class AuctionLotSerializer(AuctionLotBaseSerializer):
    favourites = serializers.SerializerMethodField()

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
            "favourites",
        ]

        extra_kwargs = {"favourites": {"read_only": True}}

    def get_favorites(self, obj):
        request = self.context.get("request")
        if not request or not hasattr(request, "user"):
            return False

        user = request.user
        if not user.is_authenticated:
            return False

        return obj.favourites.filter(id=user.id).exists()


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
        auction_lot = self._get_auction_lot()

        self._validate_close_time(auction_lot)
        self._validate_initial_price(value, auction_lot)
        self._validate_offered_price(value, auction_lot)

        return value

    def _get_auction_lot(self):
        auction_lot_id = self.initial_data.get("auction_lot")
        try:
            return AuctionLot.objects.annotate(
                max_bid=Max("bids__offered_price")
            ).get(id=auction_lot_id)
        except AuctionLot.DoesNotExist:
            raise serializers.ValidationError("AuctionLot was not found.")

    @staticmethod
    def _validate_close_time(auction_lot):
        auction_lot.refresh_from_db()
        close_time = auction_lot.close_time
        current_time = timezone.now()
        print(f"current_time: {current_time}")
        print(f"close_time: {close_time}")
        if close_time <= current_time:
            raise serializers.ValidationError("The auction is already closed.")

    @staticmethod
    def _validate_initial_price(value, auction_lot):
        if value <= auction_lot.initial_price:
            raise serializers.ValidationError(
                "The bid must be higher than the initial price."
            )

    @staticmethod
    def _validate_offered_price(value, auction_lot):
        max_bid = auction_lot.max_bid or auction_lot.initial_price

        if max_bid:
            if value <= max_bid:
                raise serializers.ValidationError(
                    f"The bid must be higher than the current highest bid ({max_bid})."
                )
            if value - max_bid< auction_lot.min_step:
                raise serializers.ValidationError(
                    f"The difference between the new bid"
                    f" and the current highest bid must be "
                    f"at least {auction_lot.min_step}."
                )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image"]
