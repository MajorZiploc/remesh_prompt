from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Team(models.Model):
  members = models.ManyToManyField(User)


class Conversation(models.Model):
  title = models.CharField(max_length=250)
  date = models.DateField()
  start_time = models.TimeField(auto_now=False, auto_now_add=False)
  duration = models.DurationField()
  max_num_of_participants = models.PositiveIntegerField()
  moderator = models.ForeignKey(User, on_delete=models.CASCADE)
  team = models.ForeignKey(Team, on_delete=models.CASCADE)
