from django.contrib.auth import get_user_model
from django.db import models

import uuid


User = get_user_model()

class AuctionLot(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_time = models.DateTimeField()
    images = models.ImageField(upload_to="images/", default=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auction_lots"
    )

    @staticmethod
    def get_unique_image_name(self, filename):
        ext = filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        return unique_filename

    def save(self, *args, **kwargs):
        if self.images:
            self.images.name = self.get_unique_image_name(self.images.name)
        super().save(*args, **kwargs)

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
