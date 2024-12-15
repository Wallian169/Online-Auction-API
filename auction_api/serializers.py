from rest_framework import serializers

from auction_api.models import AuctionLot


class BaseAuctionLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionLot
        fields = "item_name, description", "initial_price, owner"

