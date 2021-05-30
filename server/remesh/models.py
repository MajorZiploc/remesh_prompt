from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversation(models.Model):
  title = models.CharField(max_length=250)
  start_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)

  class Meta():
    ordering = ['title']


class Message(models.Model):
  text = models.TextField()
  date_time_sent = models.DateTimeField(auto_now_add=True)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

  class Meta():
    ordering = ['text']


class Thought(models.Model):
  text = models.TextField()
  date_time_sent = models.DateTimeField(auto_now_add=True)
  message = models.ForeignKey(Message, on_delete=models.CASCADE)

  class Meta():
    ordering = ['text']
