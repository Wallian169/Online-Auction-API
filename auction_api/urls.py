from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auction_api.views import AuctionLotViewSet, BidListCreateView

router = DefaultRouter()
router.register("auction-lots", AuctionLotViewSet, basename="auction-lots")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "auction-lots/<int:pk>/bids/",
        BidListCreateView.as_view(),
        name="bid-list-create"
    ),
]

app_name = "auction_api"