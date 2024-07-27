from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField("Phone", max_length=16, unique=True)
    date_joined = models.DateTimeField("Date joined", auto_now_add=True)
    is_active = models.BooleanField("Activated", default=False)
    is_staff = models.BooleanField("Staff", default=False)

    objects = UserManager()  # custom user manager

    USERNAME_FIELD = "phone"  # login field

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
