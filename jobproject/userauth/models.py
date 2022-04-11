from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="Email", unique=True)
    full_name = models.CharField(verbose_name="Full Name", max_length=200)
    phone_number = models.PositiveIntegerField(
        verbose_name="Phone Number", null=True, blank=True)
    address = models.TextField(verbose_name="Address")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def tokens(self):
        refreshtoken = RefreshToken.for_user(self)

        return {
            'refresh': str(refreshtoken),
            'access': str(refreshtoken.access_token)
        }
