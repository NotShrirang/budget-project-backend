from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    

    def __str__(self):
        return self.email