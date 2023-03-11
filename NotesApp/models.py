from django.db import models
from datetime import datetime, timedelta
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from UserAuth.models import User
import _datetime


class LabelsModel(models.Model):

    label_name = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label_name

class NotesModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collaborator = models.ManyToManyField(User, related_name='collaborater')
    label = models.ManyToManyField(LabelsModel)
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    colour = models.CharField(max_length=10, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    #image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        #ordering = ('id',)
        verbose_name = "Note"
# Create your models here.
