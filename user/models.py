from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    full_name = models.CharField(max_length=255)
    email = models.EmailField(
        "Email Address",
        unique=True,
    )
    phone_number = PhoneNumberField(blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name
