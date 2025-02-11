from django.contrib import admin

from auction_api.models import AuctionLot, Bid, AuctionLotImage, Category


@admin.register(AuctionLot)
class AuctionLotAdmin(admin.ModelAdmin):
    exclude = ("winner",)


admin.site.register(Bid)
admin.site.register(AuctionLotImage)
admin.site.register(Category)
