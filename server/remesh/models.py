from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversation(models.Model):
  title = models.CharField(max_length=250)
  start_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)

  def __str__(self):
    return self.title

  class Meta():
    ordering = ['title']


class Message(models.Model):
  text = models.TextField()
  date_time_sent = models.DateTimeField(auto_now=False, auto_now_add=False)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

  def __str__(self):
    return self.text

  class Meta():
    ordering = ['text']


class Thought(models.Model):
  text = models.TextField()
  date_time_sent = models.DateTimeField(auto_now=False, auto_now_add=False)
  message = models.ForeignKey(Message, on_delete=models.CASCADE)

  def __str__(self):
    return self.text

  class Meta():
    ordering = ['text']
