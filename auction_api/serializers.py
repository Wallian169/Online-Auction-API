from django.db.models import Max
from django.utils import timezone
from rest_framework import serializers

from auction_api.models import AuctionLot, Bid, Category, AuctionLotImage


class AuctionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionLotImage
        fields = [
            "image",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image"]


class AuctionLotBaseSerializer(serializers.ModelSerializer):
    images = AuctionImageSerializer(many=True, read_only=True)
    images_to_upload = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True,
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = AuctionLot
        fields = [
            "item_name",
            "description",
            "location",
            "category",
            "initial_price",
            "min_step",
            "buyout_price",
            "close_time",
            "images",
            "images_to_upload"
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
                errors["buyout_price"] = (
                    "Buyout price must be greater than initial price."
                )

    @staticmethod
    def _validate_close_time(data, errors):
        print(data["close_time"])
        if data["close_time"] <= timezone.now():
            errors["close_time"] = "Close time must be in the future."

    def create(self, validated_data):
        images_to_upload = validated_data.pop("images_to_upload", [])
        lot = AuctionLot.objects.create(**validated_data)
        for image in images_to_upload:
            AuctionLotImage.objects.create(
                lot=lot,
                image=image
        )
        return lot

    def update(self, instance, validated_data):
        images_to_upload = validated_data.pop("images_to_upload", [])

        for img in instance.images.all():
            img.delete()

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        for image in images_to_upload:
            AuctionLotImage.objects.create(lot=instance, image=image)

        return instance


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


class AuctionLotListSerializer(AuctionLotBaseSerializer):
    class Meta:
        model = AuctionLot
        fields = ["id", "item_name", "initial_price", "images"]


class AuctionLotDetailSerializer(AuctionLotBaseSerializer):
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
            "images",
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
            return AuctionLot.objects.annotate(max_bid=Max("bids__offered_price")).get(
                id=auction_lot_id
            )
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
            if value - max_bid < auction_lot.min_step:
                raise serializers.ValidationError(
                    f"The difference between the new bid"
                    f" and the current highest bid must be "
                    f"at least {auction_lot.min_step}."
                )
