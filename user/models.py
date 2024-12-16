from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
