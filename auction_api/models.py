from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class AuctionLot(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_time = models.DateTimeField(default=timezone.now() + timedelta(days=7))
    images = models.ImageField(upload_to="images/", default=None)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auction_lots"
    )

    def __str__(self):
        return self.item_name

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    auction_lot = models.ForeignKey(AuctionLot, related_name="bids", on_delete=models.CASCADE)
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} - {self.offered_price}"
