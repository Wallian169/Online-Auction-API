from django.urls import path
from auction_api import views

urlpatterns = [
    path("auction-lots/", views.AuctionLotListCreateView.as_view(), name="auction-lot-list-create"),
    path("auction-lots/<int:pk>/", views.AuctionLotDetailView.as_view(), name="auction-lot-detail"),
    path("auction-lots/<int:pk>/bids/", views.BidListCreateView.as_view(), name="bid-list-create"),
]

app_name = "auction_api"