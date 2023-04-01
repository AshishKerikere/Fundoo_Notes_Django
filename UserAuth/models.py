
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    location = models.CharField(max_length = 250, null=True)
    phone = models.IntegerField(null=True)


class UserLog(models.Model):
    method = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.method} {self.url}"
# Create your models here.
