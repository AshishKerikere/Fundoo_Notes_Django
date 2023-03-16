from django.db import models
from datetime import datetime, timedelta
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from UserAuth.models import User
import _datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule


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
    collaborator = models.ManyToManyField(User, related_name='collaborater', default=True)
    label = models.ManyToManyField(LabelsModel, default=True)
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    colour = models.CharField(max_length=10, null=True)
    reminder = models.DateTimeField(null=True, blank=True)
    #image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        #ordering = ('id',)
        verbose_name = "Note"
# Create your models here.

@receiver(post_save, sender=NotesModel)
def reminder_func(sender, instance, **kwargs):
    if instance.reminder:
        print(instance.reminder)
        current_date = datetime.now()
        reminder_date = instance.reminder.date()
        no_of_days = (reminder_date - current_date.date()).days
        reminder_time = datetime.now() + timedelta(days=no_of_days)
        # Schedule the reminder task using Celery
        schedule_task(instance, reminder_time)


def schedule_task(instance, reminder_time):
    schedule, created = CrontabSchedule.objects.get_or_create(
        hour=instance.reminder.hour,
        minute=instance.reminder.minute,
        day_of_month=reminder_time.day,  # 1-31 and we will not able to give no of days
        month_of_year=instance.reminder.month
    )

    existing_task = PeriodicTask.objects.filter(name=f"Task for note {instance.id}")
    if existing_task.exists():
        existing_task = existing_task.first()
        existing_task.crontab = schedule
        existing_task.save()
    else:
        PeriodicTask.objects.create(
            crontab=schedule,
            name=f"Task for note {instance.id}",
            task='NotesApp.tasks.send_mail_func',
            args=json.dumps([
                instance.title,
                instance.description,
                [instance.user.email]])
            )

#https://medium.com/swlh/dynamic-task-scheduling-with-django-celery-beat-f2591d52e15