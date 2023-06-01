from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    university = models.CharField(max_length=100, null=True, blank=True)

