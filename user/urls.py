from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView, ManageUserView, get_favorites, UserAuctionLotListView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", CreateUserView.as_view(), name="register"),
    path("profile/", ManageUserView.as_view(), name="profile"),
    path(
        "password-reset",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("favorites/", get_favorites, name="get_favorites"),
    path('my-lots/', UserAuctionLotListView.as_view(), name='user-auction-lots'),
]

app_name = "user"
