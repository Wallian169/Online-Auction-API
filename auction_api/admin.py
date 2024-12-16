from django.contrib import admin

from auction_api.models import AuctionLot, Bid

admin.site.register(AuctionLot)
admin.site.register(Bid)
