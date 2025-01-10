from django.contrib import admin

from auction_api.models import AuctionLot, Bid, AuctionLotImage, Category

admin.site.register(AuctionLot)
admin.site.register(Bid)
admin.site.register(AuctionLotImage)
admin.site.register(Category)
