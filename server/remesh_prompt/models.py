from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
  '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  '''
  PARTICIPANT = 1
  TEAMMEMBER = 2
  CHATMODERATOR = 3
  ADMIN = 4
  ROLE_CHOICES = (
      (PARTICIPANT, 'participant'),
      (TEAMMEMBER, 'teammember'),
      (CHATMODERATOR, 'chatmoderator'),
      (ADMIN, 'admin'),
  )

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()

class User(AbstractUser):
  roles = models.ManyToManyField(Role)


class Team(models.Model):
  name = models.CharField(max_length=250)
  members = models.ManyToManyField(User)

  class Meta():
    ordering = ['name']


class Conversation(models.Model):
  title = models.CharField(max_length=250)
  start_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
  duration = models.DurationField()
  max_num_of_participants = models.PositiveIntegerField()
  moderator = models.ForeignKey(User, on_delete=models.CASCADE)
  team = models.ForeignKey(Team, on_delete=models.CASCADE)

  def is_active(self):
    now = timezone.now()
    end_date_time = self.start_date_time + self.duration
    return self.start_date_time <= now <= end_date_time

  def is_past(self):
    now = timezone.now()
    end_date_time = self.start_date_time + self.duration
    return self.start_date_time > now

  def is_future(self):
    now = timezone.now()
    end_date_time = self.start_date_time + self.duration
    return end_date_time < now

  class Meta():
    ordering = ['title']


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
