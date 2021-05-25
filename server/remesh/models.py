from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Team(models.Model):
  name = models.CharField(max_length=250)
  members = models.ManyToManyField(User)


class Conversation(models.Model):
  title = models.CharField(max_length=250)
  date = models.DateField()
  start_time = models.TimeField(auto_now=False, auto_now_add=False)
  duration = models.DurationField()
  max_num_of_participants = models.PositiveIntegerField()
  moderator = models.ForeignKey(User, on_delete=models.CASCADE)
  team = models.ForeignKey(Team, on_delete=models.CASCADE)

class QuestionType(models.Model):
  label = models.CharField(max_length=250)


class Question(models.Model):
  type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  value = models.TextField()


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  value = models.TextField()


class Response(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  participant = models.ForeignKey(User, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
  value = models.TextField()

