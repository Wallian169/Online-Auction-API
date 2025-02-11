from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

import uuid

from django.utils import timezone

User = get_user_model()

def get_unique_image_name(
    filename: str,
) -> str:
    name, ext = filename.split(".")
    unique_filename = f"{name}-{uuid.uuid4().hex}.{ext}"
    return f"{unique_filename}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/categories', null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.image:
            self.image.name = get_unique_image_name(self.image.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class AuctionLot(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    location = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="auction_lots",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_step = models.DecimalField(max_digits=10, decimal_places=2)
    buyout_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auction_lots"
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="won_auction_lots",
        null=True,
        default=None,
    )
    favourites = models.ManyToManyField(
        User,
        related_name='favourite_lots',
        blank=True
    )

    def clean(self, *args, **kwargs):
        if self.buyout_price <= self.initial_price:
            raise ValidationError("Buyout price must be higher than the initial price.")
        if self.min_step <= 0:
            raise ValidationError("Minimum step must be greater than zero.")
        if self.close_time <= now():
            raise ValidationError("Close time must be in the future.")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} - {self.owner}"

class AuctionLotImage(models.Model):
    lot = models.ForeignKey(
        AuctionLot,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="lot_images/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image.name = get_unique_image_name(
                filename=self.image.name,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image {self.id} for {self.lot.item_name}"

class Bid(models.Model):
    auction_lot = models.ForeignKey(AuctionLot, related_name="bids", on_delete=models.CASCADE)
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.auction_lot.close_time <= timezone.now():
            raise ValidationError("Cannot place a bid on a closed auction lot.")

        if self.offered_price <= self.auction_lot.initial_price:
            raise ValidationError("The bid must be higher than the initial price.")

        max_bid = self.auction_lot.bids.exclude(id=self.id).order_by("-offered_price").first()

        if max_bid and self.offered_price <= max_bid.offered_price:
            raise ValidationError("The bid must be higher than the current highest bid.")

        if max_bid and (self.offered_price - max_bid.offered_price) < self.auction_lot.min_step:
            raise ValidationError(
                "The difference between the new bid "
                "and the current highest bid must be "
                f"at least {self.auction_lot.min_step}."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bidder} - {self.offered_price}"
