
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    """username = models.CharField(max_length=100, unique = True)
    password = models.CharField(max_length=100, unique = True)"""
    location = models.CharField(max_length = 250, null=True)
    phone = models.IntegerField(null=True)

    """class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'"""

# Create your models here.
