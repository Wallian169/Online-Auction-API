from django.urls import path, include
from rest_framework.routers import DefaultRouter

from auction_api.views import AuctionLotViewSet, BidListCreateView, main_page, CategoryListView

router = DefaultRouter()
router.register("auction-lots", AuctionLotViewSet, basename="auction-lots")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "auction-lots/<int:pk>/bids/",
        BidListCreateView.as_view(),
        name="bid-list-create",
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
]

app_name = "auction_api"
